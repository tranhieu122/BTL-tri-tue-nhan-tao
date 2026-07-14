"""
gbfs.py – GBFS (Greedy Best-First Search / Tìm kiếm tốt nhất tham lam)
  - Hàm đánh giá: f(n) = h(n)  (heuristic ước lượng chi phí đến đích)
  - Chạy nhanh, nhưng KHÔNG đảm bảo đường đi tối ưu
  - Khác Best-First/UCS: chỉ dùng h(n), bỏ qua g(n)
"""

import heapq
from graph import get_neighbors


def gbfs(graph, heuristic, start, goal):
    """
    Chạy GBFS từ start đến goal.
    Ưu tiên mở rộng đỉnh có h(n) nhỏ nhất.

    Parameters
    ----------
    heuristic : dict  –  h[node] = ước lượng chi phí từ node đến goal

    Returns
    -------
    dict: path, cost, expanded, generated, steps
    """
    counter = 0
    # (h, tie-breaker, node, path, g_actual)
    frontier = [(heuristic[start], counter, start, [start], 0)]
    visited = set()
    expanded = 0
    generated = 1
    steps = []

    while frontier:
        h_val, _, node, path, g = heapq.heappop(frontier)

        if node in visited:
            continue

        visited.add(node)
        expanded += 1
        steps.append({
            'step': expanded,
            'node': node,
            'h': h_val,
            'g': g,
            'path': '→'.join(path),
            'note': 'Goal!' if node == goal else '',
        })

        if node == goal:
            return {
                'path': path, 'cost': g,
                'expanded': expanded, 'generated': generated,
                'steps': steps,
            }

        for nb, w in get_neighbors(graph, node):
            if nb not in visited:
                counter += 1
                generated += 1
                heapq.heappush(frontier,
                               (heuristic[nb], counter, nb, path + [nb], g + w))

    return None
