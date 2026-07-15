"""
Flask Backend - API server cho ứng dụng tìm đường A* trên bản đồ Việt Nam.
Cung cấp các endpoint REST API cho frontend.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

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
# Khởi tạo Flask app
# ============================================================
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app)  # Cho phép frontend gọi API từ domain khác


@app.route('/')
def serve_frontend():
    """Serve frontend index.html."""
    return app.send_static_file('index.html')

# Khởi tạo graph và database
vietnam_graph = VietnamGraph()
db = Database()

# Nạp dữ liệu vào database nếu chưa có (không ghi đè nếu đã có)
data_path = os.path.join(os.path.dirname(__file__), 'data', 'vietnam_cities.json')
db.load_cities_from_json(data_path)

# Đồng bộ weights từ DB vào in-memory graph
db_edges = db.get_all_edges()
for edge in db_edges:
    # Update weight
    vietnam_graph.update_edge_weight(edge['city1'], edge['city2'], edge['distance'])
    # Update blocked status
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


def validate_cities(start, end):
    """Trả về lỗi đầu vào cho cặp tỉnh thành, hoặc None khi hợp lệ."""
    if not start or not end:
        return "Thiếu điểm xuất phát hoặc đích"

    city_names = vietnam_graph.get_city_names()
    if start not in city_names:
        return f"Tỉnh '{start}' không tồn tại"
    if end not in city_names:
        return f"Tỉnh '{end}' không tồn tại"
    if start == end:
        return "Điểm xuất phát và đích phải khác nhau"
    return None


def get_temporary_blocks(blocked_list):
    """Chuẩn hóa các chướng ngại trong request mà không đổi đồ thị dùng chung."""
    if not isinstance(blocked_list, list):
        return set()

    blocked_edges = set()
    for edge in blocked_list:
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            continue
        city1, city2 = edge
        if city1 != city2 and vietnam_graph.has_edge(city1, city2):
            blocked_edges.add(frozenset({city1, city2}))
    return blocked_edges


# ============================================================
# API Endpoints
# ============================================================

@app.route('/api/graph', methods=['GET'])
def get_graph():
    """Lấy toàn bộ dữ liệu đồ thị (nodes + edges)."""
    data = vietnam_graph.get_all_data()
    return jsonify(data)


@app.route('/api/pathfind', methods=['POST'])
def pathfind():
    """
    Tìm đường đi bằng thuật toán được chọn.
    
    Request JSON:
        {
            "start": "Hà Nội",
            "end": "Hồ Chí Minh",
            "algorithm": "astar",
            "blocked_edges": [["Thanh Hóa", "Vinh"], ...]
        }
    """
    data = request.get_json() or {}

    start = data.get('start')
    end = data.get('end')
    algo_name = data.get('algorithm', 'astar')
    blocked_list = data.get('blocked_edges', [])

    validation_error = validate_cities(start, end)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    if algo_name not in ALGORITHMS:
        return jsonify({"error": f"Thuật toán '{algo_name}' không hợp lệ"}), 400

    blocked_edges = get_temporary_blocks(blocked_list)

    adj = vietnam_graph.get_adjacency(blocked_edges)

    # Tạo heuristic function cho thuật toán cần (nhân 0.6 để đảm bảo tính Admissible do khoảng cách một số cạnh bị nhập ngắn hơn đường chim bay)
    def heuristic(city):
        coords = vietnam_graph.get_coords(city)
        end_coords = vietnam_graph.get_coords(end)
        if coords and end_coords:
            return haversine_distance(coords[0], coords[1], end_coords[0], end_coords[1]) * 0.6
        return 0

    import time
    
    # Chạy thuật toán lần đầu để lấy kết quả (đường đi, số node, v.v.)
    algo_func = ALGORITHMS[algo_name]
    if algo_name in INFORMED_ALGORITHMS:
        result = algo_func(adj, start, end, heuristic, blocked_edges)
        
        # Chạy thêm 2 lần nữa để tính thời gian trung bình (vì thời gian quá nhỏ)
        start_time = time.perf_counter()
        for _ in range(2):
            algo_func(adj, start, end, heuristic, blocked_edges)
        end_time = time.perf_counter()
    else:
        result = algo_func(adj, start, end, None, blocked_edges)
        
        # Chạy thêm 2 lần nữa để tính thời gian trung bình
        start_time = time.perf_counter()
        for _ in range(2):
            algo_func(adj, start, end, None, blocked_edges)
        end_time = time.perf_counter()

    # Tính trung bình (bao gồm cả lần chạy đầu tiên đã có thời gian trong result['time_ms'])
    total_time_ms = result.get('time_ms', 0) + ((end_time - start_time) * 1000)
    avg_time_ms = total_time_ms / 3.0
    result['time_ms'] = round(avg_time_ms, 4)

    # Lưu lịch sử
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

    return jsonify(result)


@app.route('/api/compare', methods=['POST'])
def compare_algorithms():
    """
    So sánh tất cả thuật toán cho cùng một bài toán.
    
    Request JSON:
        {
            "start": "Hà Nội",
            "end": "Hồ Chí Minh",
            "blocked_edges": [...]
        }
    """
    data = request.get_json() or {}

    start = data.get('start')
    end = data.get('end')
    blocked_list = data.get('blocked_edges', [])

    validation_error = validate_cities(start, end)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    blocked_edges = get_temporary_blocks(blocked_list)

    adj = vietnam_graph.get_adjacency(blocked_edges)

    def heuristic(city):
        coords = vietnam_graph.get_coords(city)
        end_coords = vietnam_graph.get_coords(end)
        if coords and end_coords:
            return haversine_distance(coords[0], coords[1], end_coords[0], end_coords[1]) * 0.6
        return 0

    results = []
    num_runs = 3
    
    for algo_name, algo_func in ALGORITHMS.items():
        total_time_ms = 0
        last_result = None
        
        for _ in range(num_runs):
            if algo_name in INFORMED_ALGORITHMS:
                result = algo_func(adj, start, end, heuristic, blocked_edges)
            else:
                result = algo_func(adj, start, end, None, blocked_edges)
            total_time_ms += result.get('time_ms', 0)
            last_result = result
            
        avg_time_ms = total_time_ms / num_runs

        # Chỉ trả về tóm tắt, không gửi steps chi tiết
        results.append({
            "algorithm": last_result.get('algorithm', algo_name),
            "type": last_result.get('type', 'unknown'),
            "path": last_result.get('path', []),
            "cost": last_result.get('cost', -1),
            "explored_count": last_result.get('explored_count', 0),
            "steps_count": len(last_result.get('exploration_steps', [])),
            "time_ms": round(avg_time_ms, 3)
        })

    return jsonify({"results": results})


@app.route('/api/route-insights', methods=['POST'])
def route_insights():
    """Đánh giá các cạnh trọng yếu bằng cách thử chặn từng cạnh của đường tối ưu."""
    data = request.get_json() or {}
    start = data.get('start')
    end = data.get('end')
    validation_error = validate_cities(start, end)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    blocked_edges = get_temporary_blocks(data.get('blocked_edges', []))
    baseline = dijkstra_search(
        vietnam_graph.get_adjacency(blocked_edges), start, end, None, blocked_edges
    )
    if baseline['cost'] < 0:
        return jsonify({"error": "Không có đường đi để phân tích"}), 422

    critical_links = []
    for city1, city2 in zip(baseline['path'], baseline['path'][1:]):
        disruption = blocked_edges | {frozenset({city1, city2})}
        alternative = dijkstra_search(
            vietnam_graph.get_adjacency(disruption), start, end, None, disruption
        )
        alternative_cost = alternative['cost']
        critical_links.append({
            "from": city1,
            "to": city2,
            "alternative_cost": alternative_cost,
            "extra_distance": round(max(0, alternative_cost - baseline['cost']), 2) if alternative_cost >= 0 else None,
            "status": "Mất kết nối" if alternative_cost < 0 else "Có đường vòng"
        })

    critical_links.sort(
        key=lambda link: (link['alternative_cost'] < 0, link['extra_distance'] or 0),
        reverse=True
    )
    return jsonify({
        "baseline_cost": baseline['cost'],
        "baseline_path": baseline['path'],
        "tested_links": len(critical_links),
        "critical_links": critical_links[:3]
    })


@app.route('/api/obstacles', methods=['POST'])
def manage_obstacles():
    """
    Thêm/xóa chướng ngại vật trên cạnh.
    
    Request JSON:
        {
            "action": "block" | "unblock" | "clear",
            "city1": "Thanh Hóa",
            "city2": "Vinh"
        }
    """
    data = request.get_json() or {}
    action = data.get('action', 'block')

    if action == 'clear':
        vietnam_graph.clear_all_blocks()
        db.clear_all_blocks()
        return jsonify({"message": "Đã gỡ tất cả chướng ngại vật"})

    city1 = data.get('city1')
    city2 = data.get('city2')

    if not city1 or not city2:
        return jsonify({"error": "Thiếu thông tin tỉnh thành"}), 400

    if not vietnam_graph.has_edge(city1, city2):
        return jsonify({"error": f"Không có tuyến đường trực tiếp giữa {city1} và {city2}"}), 404

    if action == 'block':
        vietnam_graph.block_edge(city1, city2)
        city1_id = vietnam_graph.get_city_id(city1)
        city2_id = vietnam_graph.get_city_id(city2)
        if city1_id and city2_id:
            db.set_edge_blocked(city1_id, city2_id, True)
        return jsonify({"message": f"Đã chặn đường {city1} - {city2}"})

    elif action == 'unblock':
        vietnam_graph.unblock_edge(city1, city2)
        city1_id = vietnam_graph.get_city_id(city1)
        city2_id = vietnam_graph.get_city_id(city2)
        if city1_id and city2_id:
            db.set_edge_blocked(city1_id, city2_id, False)
        return jsonify({"message": f"Đã mở đường {city1} - {city2}"})

    return jsonify({"error": "Action không hợp lệ"}), 400


@app.route('/api/edge/weight', methods=['POST'])
def update_edge_weight():
    """
    Cập nhật trọng số của cạnh.
    
    Request JSON:
        {
            "city1": "Hà Nội",
            "city2": "Bắc Ninh",
            "weight": 100
        }
    """
    data = request.get_json() or {}
    city1 = data.get('city1')
    city2 = data.get('city2')
    weight = data.get('weight')

    if not city1 or not city2 or weight is None:
        return jsonify({"error": "Thiếu thông tin hoặc trọng số"}), 400

    try:
        weight = float(weight)
        if weight <= 0:
            return jsonify({"error": "Trọng số phải lớn hơn 0"}), 400
    except ValueError:
        return jsonify({"error": "Trọng số không hợp lệ"}), 400

    # Update in memory
    success = vietnam_graph.update_edge_weight(city1, city2, weight)
    if not success:
        return jsonify({"error": f"Không tìm thấy đường nối giữa {city1} và {city2}"}), 404

    # Update in DB
    city1_id = vietnam_graph.get_city_id(city1)
    city2_id = vietnam_graph.get_city_id(city2)
    if city1_id and city2_id:
        db.update_edge_weight(city1_id, city2_id, weight)

    return jsonify({"message": f"Đã cập nhật khoảng cách {city1} - {city2} thành {weight}km"})



@app.route('/api/history', methods=['GET'])
def get_history():
    """Lấy lịch sử tìm kiếm."""
    limit = request.args.get('limit', 50, type=int)
    history = db.get_search_history(limit)
    return jsonify({"history": history})


@app.route('/api/cities', methods=['GET'])
def get_cities():
    """Lấy danh sách tên tỉnh thành."""
    return jsonify({"cities": vietnam_graph.get_city_names()})


# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    print("=" * 60)
    print("  🗺️  Vietnam A* Pathfinding API Server")
    print("  📍 34 đơn vị cấp tỉnh + Hoàng Sa, Trường Sa | 6 thuật toán")
    print("  🌐 http://localhost:5000")
    print("=" * 60)
    # Disable the file reloader because each search writes SQLite history,
    # which would otherwise trigger an unnecessary server restart in debug mode.
    app.run(debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true', use_reloader=False, host='0.0.0.0', port=5000)
