"""
Flask Backend - API server cho ứng dụng tìm đường A* trên bản đồ Việt Nam.
Phiên bản nâng cấp: validation chặt, metrics, cache, và endpoint vận hành.
"""

from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import logging
import os
import sys
import time
from threading import RLock

from flask import Flask, g, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Thêm thư mục gốc vào path
sys.path.insert(0, os.path.dirname(__file__))

from models.graph_model import VietnamGraph
from database.db import Database
from algorithms.heuristics import haversine_distance
from algorithms.astar import astar_search
from algorithms.dijkstra import dijkstra_search
from algorithms.bfs import bfs_search
from algorithms.dfs import dfs_search
from algorithms.greedy import greedy_search
from algorithms.ucs import ucs_search

# ============================================================
# Logging
# ============================================================
logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'INFO').upper(),
    format='%(asctime)s %(levelname)s %(name)s - %(message)s'
)
logger = logging.getLogger('vietnam-pathfinding-api')


# ============================================================
# Khởi tạo Flask app
# ============================================================
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')

_cors_origins_env = os.environ.get('CORS_ALLOWED_ORIGINS', '').strip()
if _cors_origins_env:
    _allowed_origins = [origin.strip() for origin in _cors_origins_env.split(',') if origin.strip()]
else:
    _allowed_origins = [
        'http://localhost:5000',
        'http://127.0.0.1:5000',
        'http://localhost:5500',
        'http://127.0.0.1:5500'
    ]
CORS(app, resources={r'/api/*': {'origins': _allowed_origins}})


@app.route('/')
def serve_frontend():
    """Serve frontend index.html."""
    return app.send_static_file('index.html')


# ============================================================
# Runtime config
# ============================================================
BENCHMARK_RUNS = max(1, int(os.environ.get('BENCHMARK_RUNS', '3')))
PATHFIND_CACHE_TTL_SEC = max(5, int(os.environ.get('PATHFIND_CACHE_TTL_SEC', '45')))
COMPARE_CACHE_TTL_SEC = max(5, int(os.environ.get('COMPARE_CACHE_TTL_SEC', '30')))
MAX_HISTORY_LIMIT = max(10, int(os.environ.get('MAX_HISTORY_LIMIT', '200')))


# ============================================================
# Runtime helpers
# ============================================================
class TTLCache:
    """Cache TTL đơn giản, thread-safe, không cần dependency ngoài."""

    def __init__(self, ttl_seconds=30, max_entries=512):
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._store = {}
        self._lock = RLock()

    def _evict_expired_locked(self):
        now = time.time()
        expired = [k for k, (expiry, _) in self._store.items() if expiry <= now]
        for key in expired:
            self._store.pop(key, None)

    def get(self, key):
        with self._lock:
            self._evict_expired_locked()
            item = self._store.get(key)
            if not item:
                return None
            expiry, value = item
            if expiry <= time.time():
                self._store.pop(key, None)
                return None
            return deepcopy(value)

    def set(self, key, value):
        with self._lock:
            self._evict_expired_locked()
            if len(self._store) >= self.max_entries:
                # Xóa item cũ nhất theo expiry
                oldest_key = min(self._store, key=lambda k: self._store[k][0])
                self._store.pop(oldest_key, None)
            self._store[key] = (time.time() + self.ttl_seconds, deepcopy(value))

    def clear(self):
        with self._lock:
            self._store.clear()

    def size(self):
        with self._lock:
            self._evict_expired_locked()
            return len(self._store)


def utc_iso_now():
    return datetime.now(timezone.utc).isoformat()


def error_response(message, status=400, code=None, details=None):
    payload = {'error': message}
    if code:
        payload['code'] = code
    if details is not None:
        payload['details'] = details
    payload['timestamp'] = utc_iso_now()
    return jsonify(payload), status


def read_json_payload():
    """Đọc payload JSON an toàn và trả về (dict, error_response)."""
    if not request.is_json:
        return None, error_response('Request phải có Content-Type: application/json', 415, 'UNSUPPORTED_MEDIA_TYPE')
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return None, error_response('JSON không hợp lệ hoặc body rỗng', 400, 'INVALID_JSON')
    return payload, None


def normalize_algorithm(name):
    return str(name or 'astar').strip().lower()


def normalize_result_type(result_type):
    if result_type == 'uninformed':
        return 'blind'
    return result_type


def clamp_limit(value, fallback=50, minimum=1, maximum=200):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return fallback
    return max(minimum, min(maximum, parsed))


def _normalize_blocks_for_cache(blocked_edges):
    normalized = []
    for edge in blocked_edges:
        city_pair = sorted(list(edge))
        if len(city_pair) == 2:
            normalized.append(city_pair)
    normalized.sort()
    return normalized


def _build_cache_key(kind, start, end, algo_name, blocked_edges):
    base_obj = {
        'kind': kind,
        'start': start,
        'end': end,
        'algorithm': algo_name,
        'blocked': _normalize_blocks_for_cache(blocked_edges),
        'graph_revision': GRAPH_REVISION
    }
    base = json.dumps(base_obj, ensure_ascii=False, sort_keys=True)
    digest = hashlib.sha256(base.encode('utf-8')).hexdigest()
    return digest


# ============================================================
# Shared state
# ============================================================
GRAPH_LOCK = RLock()
DB_LOCK = RLock()
METRICS_LOCK = RLock()

PATHFIND_CACHE = TTLCache(ttl_seconds=PATHFIND_CACHE_TTL_SEC, max_entries=1024)
COMPARE_CACHE = TTLCache(ttl_seconds=COMPARE_CACHE_TTL_SEC, max_entries=256)

GRAPH_REVISION = 0
STARTUP_TS = time.perf_counter()

METRICS = {
    'started_at': utc_iso_now(),
    'requests_total': 0,
    'errors_total': 0,
    'cache_hits': {'pathfind': 0, 'compare': 0},
    'cache_misses': {'pathfind': 0, 'compare': 0},
    'algorithm_requests': defaultdict(int),
    'endpoint': defaultdict(lambda: {'count': 0, 'errors': 0, 'avg_ms': 0.0, 'last_ms': 0.0})
}


# Khởi tạo graph và database
vietnam_graph = VietnamGraph()
db = Database()

# Nạp dữ liệu vào database nếu chưa có (không ghi đè nếu đã có)
data_path = os.path.join(os.path.dirname(__file__), 'data', 'vietnam_cities.json')
with DB_LOCK:
    db.load_cities_from_json(data_path)

# Đồng bộ weights từ DB vào in-memory graph
with DB_LOCK:
    db_edges = db.get_all_edges()
with GRAPH_LOCK:
    for edge in db_edges:
        vietnam_graph.update_edge_weight(edge['city1'], edge['city2'], edge['distance'])
        if edge['is_blocked']:
            vietnam_graph.block_edge(edge['city1'], edge['city2'])

# Map tên thuật toán -> hàm tìm kiếm
ALGORITHMS = {
    'astar': astar_search,
    'dijkstra': dijkstra_search,
    'bfs': bfs_search,
    'dfs': dfs_search,
    'greedy': greedy_search,
    'ucs': ucs_search
}

# Thuật toán cần heuristic
INFORMED_ALGORITHMS = {'astar', 'greedy'}


def invalidate_caches_and_bump_revision():
    """Xóa cache khi đồ thị thay đổi để tránh dữ liệu cũ."""
    global GRAPH_REVISION
    PATHFIND_CACHE.clear()
    COMPARE_CACHE.clear()
    with GRAPH_LOCK:
        GRAPH_REVISION += 1


def validate_cities(start, end):
    """Trả về lỗi đầu vào cho cặp tỉnh thành, hoặc None khi hợp lệ."""
    if not start or not end:
        return 'Thiếu điểm xuất phát hoặc đích'

    with GRAPH_LOCK:
        city_names = set(vietnam_graph.get_city_names())
    if start not in city_names:
        return f"Tỉnh '{start}' không tồn tại"
    if end not in city_names:
        return f"Tỉnh '{end}' không tồn tại"
    if start == end:
        return 'Điểm xuất phát và đích phải khác nhau'
    return None


def get_temporary_blocks(blocked_list):
    """Chuẩn hóa các chướng ngại trong request mà không đổi đồ thị dùng chung."""
    if not isinstance(blocked_list, list):
        return set()

    blocked_edges = set()
    with GRAPH_LOCK:
        for edge in blocked_list:
            if not isinstance(edge, (list, tuple)) or len(edge) != 2:
                continue
            city1, city2 = edge
            if city1 != city2 and vietnam_graph.has_edge(city1, city2):
                blocked_edges.add(frozenset({city1, city2}))
    return blocked_edges


def build_heuristic(end_city):
    """Tạo heuristic cho thuật toán informed với hệ số an toàn."""
    with GRAPH_LOCK:
        end_coords = vietnam_graph.get_coords(end_city)

    def heuristic(city):
        if not end_coords:
            return 0
        with GRAPH_LOCK:
            coords = vietnam_graph.get_coords(city)
        if not coords:
            return 0
        return haversine_distance(coords[0], coords[1], end_coords[0], end_coords[1]) * 0.6

    return heuristic


def run_algorithm_benchmark(algo_name, adj, start, end, heuristic, blocked_edges, runs=3):
    """Chạy thuật toán nhiều lần để lấy thời gian trung bình ổn định."""
    algo_func = ALGORITHMS[algo_name]
    measured_ms = []
    first_result = None

    for run_idx in range(runs):
        begin = time.perf_counter()
        if algo_name in INFORMED_ALGORITHMS:
            result = algo_func(adj, start, end, heuristic, blocked_edges)
        else:
            result = algo_func(adj, start, end, None, blocked_edges)
        elapsed_ms = (time.perf_counter() - begin) * 1000
        measured_ms.append(elapsed_ms)
        if run_idx == 0:
            first_result = result

    first_result['time_ms'] = round(sum(measured_ms) / len(measured_ms), 4)
    if 'type' in first_result:
        first_result['type'] = normalize_result_type(first_result.get('type'))
    return first_result


# ============================================================
# Request lifecycle instrumentation
# ============================================================
@app.before_request
def before_api_request():
    if request.path.startswith('/api/'):
        g.request_started = time.perf_counter()


@app.after_request
def after_api_request(response):
    if request.path.startswith('/api/') and hasattr(g, 'request_started'):
        elapsed_ms = (time.perf_counter() - g.request_started) * 1000
        endpoint_name = request.endpoint or request.path

        with METRICS_LOCK:
            METRICS['requests_total'] += 1
            bucket = METRICS['endpoint'][endpoint_name]
            bucket['count'] += 1
            bucket['last_ms'] = round(elapsed_ms, 3)
            bucket['avg_ms'] = round(
                ((bucket['avg_ms'] * (bucket['count'] - 1)) + elapsed_ms) / bucket['count'],
                3
            )
            if response.status_code >= 400:
                METRICS['errors_total'] += 1
                bucket['errors'] += 1

        response.headers['X-Process-Time-Ms'] = f'{elapsed_ms:.3f}'
    return response


@app.errorhandler(HTTPException)
def handle_http_exception(error):
    """Đảm bảo mọi lỗi HTTP trả về JSON thống nhất."""
    return error_response(error.description, status=error.code, code=error.name)


@app.errorhandler(Exception)
def handle_unexpected_exception(error):
    """Fallback cho lỗi không dự đoán trước."""
    logger.exception('Unhandled exception: %s', error)
    return error_response('Lỗi nội bộ máy chủ', status=500, code='INTERNAL_SERVER_ERROR')


# ============================================================
# API Endpoints
# ============================================================
@app.route('/api/graph', methods=['GET'])
def get_graph():
    """Lấy toàn bộ dữ liệu đồ thị (nodes + edges)."""
    with GRAPH_LOCK:
        data = vietnam_graph.get_all_data()
    data['graph_revision'] = GRAPH_REVISION
    return jsonify(data)


@app.route('/api/pathfind', methods=['POST'])
def pathfind():
    """Tìm đường đi bằng thuật toán được chọn."""
    data, payload_error = read_json_payload()
    if payload_error:
        return payload_error

    start = str(data.get('start', '')).strip()
    end = str(data.get('end', '')).strip()
    algo_name = normalize_algorithm(data.get('algorithm', 'astar'))
    blocked_list = data.get('blocked_edges', [])

    validation_error = validate_cities(start, end)
    if validation_error:
        return error_response(validation_error, 400, 'INVALID_CITY_INPUT')

    if algo_name not in ALGORITHMS:
        return error_response(f"Thuật toán '{algo_name}' không hợp lệ", 400, 'INVALID_ALGORITHM')

    blocked_edges = get_temporary_blocks(blocked_list)
    cache_key = _build_cache_key('pathfind', start, end, algo_name, blocked_edges)
    cached_result = PATHFIND_CACHE.get(cache_key)
    if cached_result:
        cached_result['cached'] = True
        with METRICS_LOCK:
            METRICS['cache_hits']['pathfind'] += 1
            METRICS['algorithm_requests'][algo_name] += 1
        return jsonify(cached_result)

    with METRICS_LOCK:
        METRICS['cache_misses']['pathfind'] += 1
        METRICS['algorithm_requests'][algo_name] += 1

    with GRAPH_LOCK:
        adj = vietnam_graph.get_adjacency(blocked_edges)
    heuristic = build_heuristic(end)

    result = run_algorithm_benchmark(
        algo_name=algo_name,
        adj=adj,
        start=start,
        end=end,
        heuristic=heuristic,
        blocked_edges=blocked_edges,
        runs=BENCHMARK_RUNS
    )
    result['cached'] = False

    with DB_LOCK:
        try:
            db.save_search_result(
                algorithm=result.get('algorithm', algo_name),
                start=start,
                end=end,
                path=result.get('path', []),
                distance=result.get('cost', -1),
                time_ms=result.get('time_ms', 0),
                nodes_explored=result.get('explored_count', 0),
                steps_count=len(result.get('exploration_steps', []))
            )
        except Exception as db_error:  # pragma: no cover
            logger.exception('Failed to save search history: %s', db_error)

    PATHFIND_CACHE.set(cache_key, result)
    return jsonify(result)


@app.route('/api/compare', methods=['POST'])
def compare_algorithms():
    """So sánh tất cả thuật toán cho cùng một bài toán."""
    data, payload_error = read_json_payload()
    if payload_error:
        return payload_error

    start = str(data.get('start', '')).strip()
    end = str(data.get('end', '')).strip()
    blocked_list = data.get('blocked_edges', [])

    validation_error = validate_cities(start, end)
    if validation_error:
        return error_response(validation_error, 400, 'INVALID_CITY_INPUT')

    blocked_edges = get_temporary_blocks(blocked_list)
    cache_key = _build_cache_key('compare', start, end, 'all', blocked_edges)
    cached_result = COMPARE_CACHE.get(cache_key)
    if cached_result:
        cached_result['cached'] = True
        with METRICS_LOCK:
            METRICS['cache_hits']['compare'] += 1
        return jsonify(cached_result)

    with METRICS_LOCK:
        METRICS['cache_misses']['compare'] += 1

    with GRAPH_LOCK:
        adj = vietnam_graph.get_adjacency(blocked_edges)
    heuristic = build_heuristic(end)

    results = []
    for algo_name in ALGORITHMS:
        with METRICS_LOCK:
            METRICS['algorithm_requests'][algo_name] += 1

        last_result = run_algorithm_benchmark(
            algo_name=algo_name,
            adj=adj,
            start=start,
            end=end,
            heuristic=heuristic,
            blocked_edges=blocked_edges,
            runs=BENCHMARK_RUNS
        )

        results.append({
            'algorithm': last_result.get('algorithm', algo_name),
            'type': normalize_result_type(last_result.get('type', 'unknown')),
            'path': last_result.get('path', []),
            'cost': last_result.get('cost', -1),
            'explored_count': last_result.get('explored_count', 0),
            'steps_count': len(last_result.get('exploration_steps', [])),
            'time_ms': round(last_result.get('time_ms', 0), 4)
        })

    payload = {
        'results': results,
        'benchmark_runs': BENCHMARK_RUNS,
        'cached': False
    }
    COMPARE_CACHE.set(cache_key, payload)
    return jsonify(payload)


@app.route('/api/obstacles', methods=['POST'])
def manage_obstacles():
    """Thêm/xóa chướng ngại vật trên cạnh."""
    data, payload_error = read_json_payload()
    if payload_error:
        return payload_error

    action = str(data.get('action', 'block')).strip().lower()
    if action not in {'block', 'unblock', 'clear'}:
        return error_response('Action không hợp lệ', 400, 'INVALID_ACTION')

    if action == 'clear':
        with GRAPH_LOCK:
            vietnam_graph.clear_all_blocks()
        with DB_LOCK:
            db.clear_all_blocks()
        invalidate_caches_and_bump_revision()
        return jsonify({'message': 'Đã gỡ tất cả chướng ngại vật'})

    city1 = str(data.get('city1', '')).strip()
    city2 = str(data.get('city2', '')).strip()
    if not city1 or not city2:
        return error_response('Thiếu thông tin tỉnh thành', 400, 'MISSING_CITY')

    with GRAPH_LOCK:
        if not vietnam_graph.has_edge(city1, city2):
            return error_response(f'Không có tuyến đường trực tiếp giữa {city1} và {city2}', 404, 'EDGE_NOT_FOUND')

        if action == 'block':
            vietnam_graph.block_edge(city1, city2)
        else:
            vietnam_graph.unblock_edge(city1, city2)

        city1_id = vietnam_graph.get_city_id(city1)
        city2_id = vietnam_graph.get_city_id(city2)

    if city1_id and city2_id:
        with DB_LOCK:
            db.set_edge_blocked(city1_id, city2_id, action == 'block')

    invalidate_caches_and_bump_revision()
    if action == 'block':
        return jsonify({'message': f'Đã chặn đường {city1} - {city2}'})
    return jsonify({'message': f'Đã mở đường {city1} - {city2}'})


@app.route('/api/edge/weight', methods=['POST'])
def update_edge_weight():
    """Cập nhật trọng số của cạnh."""
    data, payload_error = read_json_payload()
    if payload_error:
        return payload_error

    city1 = str(data.get('city1', '')).strip()
    city2 = str(data.get('city2', '')).strip()
    weight = data.get('weight')

    if not city1 or not city2 or weight is None:
        return error_response('Thiếu thông tin hoặc trọng số', 400, 'MISSING_FIELDS')

    try:
        weight = float(weight)
    except (TypeError, ValueError):
        return error_response('Trọng số không hợp lệ', 400, 'INVALID_WEIGHT')

    if weight <= 0:
        return error_response('Trọng số phải lớn hơn 0', 400, 'INVALID_WEIGHT_RANGE')
    if weight > 5000:
        return error_response('Trọng số quá lớn, vui lòng nhập giá trị hợp lý', 400, 'INVALID_WEIGHT_RANGE')

    with GRAPH_LOCK:
        success = vietnam_graph.update_edge_weight(city1, city2, weight)
        if not success:
            return error_response(f'Không tìm thấy đường nối giữa {city1} và {city2}', 404, 'EDGE_NOT_FOUND')

        city1_id = vietnam_graph.get_city_id(city1)
        city2_id = vietnam_graph.get_city_id(city2)

    if city1_id and city2_id:
        with DB_LOCK:
            db.update_edge_weight(city1_id, city2_id, weight)

    invalidate_caches_and_bump_revision()
    return jsonify({'message': f'Đã cập nhật khoảng cách {city1} - {city2} thành {weight}km'})


@app.route('/api/history', methods=['GET'])
def get_history():
    """Lấy lịch sử tìm kiếm."""
    limit = clamp_limit(
        request.args.get('limit', 50),
        fallback=50,
        minimum=1,
        maximum=MAX_HISTORY_LIMIT
    )
    with DB_LOCK:
        history = db.get_search_history(limit)
    return jsonify({'history': history})


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """Xóa toàn bộ lịch sử tìm kiếm để reset môi trường demo."""
    with DB_LOCK:
        db.clear_search_history()
    return jsonify({'message': 'Đã xóa toàn bộ lịch sử tìm kiếm'})


@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Lấy danh sách tên tỉnh thành."""
    with GRAPH_LOCK:
        cities = vietnam_graph.get_city_names()
    return jsonify({'cities': cities})


@app.route('/api/health', methods=['GET'])
def health():
    """Health endpoint cho monitoring hoặc kiểm tra nhanh trạng thái hệ thống."""
    with DB_LOCK:
        graph_stats = db.get_graph_stats()
        history_count = db.count_search_history()

    payload = {
        'status': 'ok',
        'timestamp': utc_iso_now(),
        'uptime_sec': round(time.perf_counter() - STARTUP_TS, 2),
        'graph_revision': GRAPH_REVISION,
        'graph': graph_stats,
        'history_count': history_count,
        'cache': {
            'pathfind_entries': PATHFIND_CACHE.size(),
            'compare_entries': COMPARE_CACHE.size()
        },
        'benchmark_runs': BENCHMARK_RUNS
    }
    return jsonify(payload)


@app.route('/api/metrics', methods=['GET'])
def metrics():
    """Metrics endpoint dạng JSON để quan sát hiệu năng backend."""
    with METRICS_LOCK:
        endpoint_snapshot = {
            key: dict(value)
            for key, value in METRICS['endpoint'].items()
        }
        algo_snapshot = dict(METRICS['algorithm_requests'])
        payload = {
            'started_at': METRICS['started_at'],
            'uptime_sec': round(time.perf_counter() - STARTUP_TS, 2),
            'requests_total': METRICS['requests_total'],
            'errors_total': METRICS['errors_total'],
            'cache_hits': dict(METRICS['cache_hits']),
            'cache_misses': dict(METRICS['cache_misses']),
            'algorithm_requests': algo_snapshot,
            'endpoint': endpoint_snapshot,
            'graph_revision': GRAPH_REVISION,
            'cache_size': {
                'pathfind_entries': PATHFIND_CACHE.size(),
                'compare_entries': COMPARE_CACHE.size()
            }
        }
    return jsonify(payload)


@app.route('/api/admin/cache/clear', methods=['POST'])
def clear_runtime_cache():
    """Xóa cache runtime theo yêu cầu quản trị."""
    PATHFIND_CACHE.clear()
    COMPARE_CACHE.clear()
    return jsonify({'message': 'Đã xóa cache runtime'})


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print('=' * 60)
    print('  🗺️  Vietnam A* Pathfinding API Server')
    print('  📍 34 đơn vị cấp tỉnh + Hoàng Sa, Trường Sa | 6 thuật toán')
    print('  🌐 http://localhost:5000')
    print('=' * 60)
    # Disable reloader để tránh restart không cần thiết khi SQLite thay đổi file.
    app.run(
        debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true',
        use_reloader=False,
        host='0.0.0.0',
        port=5000
    )
