"""
main.py – Chạy và in chi tiết 6 thuật toán tìm kiếm trên đồ thị G1,
          kèm bảng tổng hợp và đo thời gian trung bình (20 lần).

Cấu trúc dự án:
    graph.py        – Định nghĩa đồ thị G1 và heuristic
    bfs.py          – BFS  (f = không có, tìm kiếm mù theo chiều rộng)
    dfs.py          – DFS  (f = không có, tìm kiếm mù theo chiều sâu)
    ids.py          – IDS  (Iterative Deepening Search)
    best_first.py   – Best-First / UCS  (f = g(n), không dùng heuristic)
    gbfs.py         – GBFS  (f = h(n), tham lam theo heuristic)
    astar.py        – A*  (f = g(n) + h(n))
    benchmark.py    – Đo hiệu năng, xuất result.csv
    main.py         – Điểm vào chính (file này)
"""

import time

from graph      import G1_GRAPH, G1_HEURISTIC, G1_START, G1_GOAL
from bfs        import bfs
from dfs        import dfs
from ids        import ids
from best_first import best_first
from gbfs       import gbfs
from astar      import astar

RUNS = 20   # số lần chạy để đo thời gian trung bình


# ══════════════════════════════════════════════════════════════════════════════
# Tiện ích in bảng
# ══════════════════════════════════════════════════════════════════════════════

def print_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))

    def fmt(row):
        return ' | '.join(str(c).ljust(widths[i]) for i, c in enumerate(row))

    sep = '-+-'.join('-' * w for w in widths)
    print(fmt(headers))
    print(sep)
    for row in rows:
        print(fmt(row))
    print()


def print_header(title):
    print()
    print('═' * 72)
    print(f'  {title}')
    print('═' * 72)


def print_result_summary(result, name):
    if result is None:
        print(f'  [{name}] ✗ Không tìm thấy đường đi!\n')
        return
    print(f'  Đường đi : {" → ".join(result["path"])}')
    print(f'  Chi phí  : {result["cost"]}')
    print(f'  Node mở  : {result["expanded"]}')
    print(f'  Node sinh: {result["generated"]}')
    print()


# ══════════════════════════════════════════════════════════════════════════════
# Hàm hiển thị chi tiết từng thuật toán
# ══════════════════════════════════════════════════════════════════════════════

def show_bfs(result):
    print_header('BFS – Breadth-First Search  (không có heuristic)')
    rows = [[s['step'], s['node'], s['path'], s['cost'], s['note']]
            for s in result['steps']]
    print_table(['Bước', 'Đỉnh', 'Đường đi', 'Chi phí', 'Ghi chú'], rows)
    print_result_summary(result, 'BFS')


def show_dfs(result):
    print_header('DFS – Depth-First Search  (không có heuristic)')
    rows = [[s['step'], s['node'], s['path'], s['cost'], s['note']]
            for s in result['steps']]
    print_table(['Bước', 'Đỉnh', 'Đường đi', 'Chi phí', 'Ghi chú'], rows)
    print_result_summary(result, 'DFS')


def show_ids(result):
    print_header('IDS – Iterative Deepening Search  (không có heuristic)')
    for depth, steps in result['steps_by_depth'].items():
        print(f'  ── Giới hạn độ sâu = {depth} ──')
        rows = [[s['step'], s['node'], s['depth'], s['path'], s['cost'], s['note']]
                for s in steps]
        print_table(['Bước', 'Đỉnh', 'Độ sâu', 'Đường đi', 'Chi phí', 'Ghi chú'], rows)
    print(f'  Tìm thấy ở giới hạn độ sâu = {result["depth_found"]}')
    print_result_summary(result, 'IDS')


def show_best_first(result):
    print_header('Best-First Search / UCS  [f(n) = g(n)]')
    rows = [[s['step'], s['node'], s['g'], s['path'], s['note']]
            for s in result['steps']]
    print_table(['Bước', 'Đỉnh', 'g(n)', 'Đường đi', 'Ghi chú'], rows)
    print_result_summary(result, 'Best-First')


def show_gbfs(result):
    print_header('GBFS – Greedy Best-First Search  [f(n) = h(n)]')
    rows = [[s['step'], s['node'], s['h'], s['g'], s['path'], s['note']]
            for s in result['steps']]
    print_table(['Bước', 'Đỉnh', 'h(n)', 'Chi phí thực', 'Đường đi', 'Ghi chú'], rows)
    print_result_summary(result, 'GBFS')


def show_astar(result):
    print_header('A* Search  [f(n) = g(n) + h(n)]')
    rows = [[s['step'], s['node'], s['g'], s['h'], s['f'], s['path'], s['note']]
            for s in result['steps']]
    print_table(['Bước', 'Đỉnh', 'g(n)', 'h(n)', 'f(n)', 'Đường đi', 'Ghi chú'], rows)
    print_result_summary(result, 'A*')


# ══════════════════════════════════════════════════════════════════════════════
# Đo thời gian trung bình
# ══════════════════════════════════════════════════════════════════════════════

def measure_avg_ms(algo_fn):
    times = []
    for _ in range(RUNS):
        t0 = time.perf_counter()
        algo_fn()
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return round((sum(times) / RUNS) * 1000, 4)


# ══════════════════════════════════════════════════════════════════════════════
# Bảng tổng hợp kết quả
# ══════════════════════════════════════════════════════════════════════════════

def print_summary(rows):
    print()
    print('═' * 72)
    print('  BẢNG TỔNG HỢP KẾT QUẢ  (thời gian trung bình qua 20 lần chạy)')
    print('═' * 72)
    headers = ['Thuật toán', 'Đường đi', 'Chi phí',
               'Node mở', 'Node sinh', 'TG TB (ms)']
    print_table(headers, rows)


def make_row(name, result, t_ms):
    if result:
        return [name, '→'.join(result['path']), result['cost'],
                result['expanded'], result['generated'], t_ms]
    return [name, '-', '-', '-', '-', t_ms]


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    g, h = G1_GRAPH, G1_HEURISTIC
    s, goal = G1_START, G1_GOAL

    print()
    print('╔' + '═' * 70 + '╗')
    print('║  KIỂM TRA GIỮA KỲ – TRÍ TUỆ NHÂN TẠO'.ljust(71) + '║')
    print('║  Đồ thị G1  |  Đỉnh đầu: S  |  Đỉnh đích: G'.ljust(71) + '║')
    print('╚' + '═' * 70 + '╝')

    # ── Chạy thuật toán ──────────────────────────────────────────────────────
    r_bfs  = bfs(g, s, goal)
    r_dfs  = dfs(g, s, goal)
    r_ids  = ids(g, s, goal)
    r_bf   = best_first(g, s, goal)
    r_gbfs = gbfs(g, h, s, goal)
    r_ast  = astar(g, h, s, goal)

    # ── In chi tiết từng thuật toán ───────────────────────────────────────────
    show_bfs(r_bfs)
    show_dfs(r_dfs)
    show_ids(r_ids)
    show_best_first(r_bf)
    show_gbfs(r_gbfs)
    show_astar(r_ast)

    # ── Đo thời gian trung bình ───────────────────────────────────────────────
    t_bfs  = measure_avg_ms(lambda: bfs(g, s, goal))
    t_dfs  = measure_avg_ms(lambda: dfs(g, s, goal))
    t_ids  = measure_avg_ms(lambda: ids(g, s, goal))
    t_bf   = measure_avg_ms(lambda: best_first(g, s, goal))
    t_gbfs = measure_avg_ms(lambda: gbfs(g, h, s, goal))
    t_ast  = measure_avg_ms(lambda: astar(g, h, s, goal))

    summary_rows = [
        make_row('DFS',        r_dfs,  t_dfs),
        make_row('BFS',        r_bfs,  t_bfs),
        make_row('IDS',        r_ids,  t_ids),
        make_row('Best-First', r_bf,   t_bf),
        make_row('GBFS',       r_gbfs, t_gbfs),
        make_row('A*',         r_ast,  t_ast),
    ]
    print_summary(summary_rows)

    # ── Kết luận ─────────────────────────────────────────────────────────────
    print('  KẾT LUẬN:')
    print('  - DFS       : mở rộng ít node, nhanh nhưng KHÔNG tối ưu về chi phí.')
    print('  - BFS       : đảm bảo ít cạnh nhất, KHÔNG tối ưu về chi phí.')
    print('  - IDS       : như BFS về độ tối ưu, ít bộ nhớ hơn, nhưng lặp nhiều lần.')
    print('  - Best-First: tối ưu về chi phí (UCS), không cần heuristic.')
    print('  - GBFS      : nhanh nhờ heuristic, nhưng KHÔNG đảm bảo tối ưu.')
    print('  - A*        : TỐI ƯU & ĐẦY ĐỦ; mở ít node hơn UCS nhờ heuristic.')
    print()


if __name__ == '__main__':
    main()


# ══════════════════════════════════════════════════════════════════════════════
# Legacy code giữ lại để tham khảo
# ══════════════════════════════════════════════════════════════════════════════

def _legacy_placeholder():
    """Phần này đã được tái cấu trúc thành các module riêng biệt."""
