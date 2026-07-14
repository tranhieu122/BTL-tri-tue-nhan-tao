"""
best_first.py – Best-First Search / Uniform Cost Search (UCS)
  - Hàm đánh giá: f(n) = g(n)  (chi phí thực từ đầu đến n, không dùng heuristic)
  - Đảm bảo tìm đường đi TỐI ƯU VỀ CHI PHÍ (giống Dijkstra)
  - Khác GBFS: không dùng heuristic h(n)
"""

import heapq
from graph import get_neighbors


def best_first(graph, start, goal):
    """
    Chạy Best-First Search (UCS) từ start đến goal.
    Ưu tiên mở rộng đỉnh có chi phí tích lũy g(n) nhỏ nhất.

    Returns
    -------
    dict: path, cost, expanded, generated, steps
    """
    counter = 0
    # (g, tie-breaker, node, path)
    frontier = [(0, counter, start, [start])]
    best_g = {start: 0}
    expanded = 0
    generated = 1
    steps = []

    while frontier:
        g, _, node, path = heapq.heappop(frontier)

        # Bỏ qua nếu đã tìm được đường ngắn hơn đến node này
        if g > best_g.get(node, float('inf')):
            continue

        expanded += 1
        steps.append({
            'step': expanded,
            'node': node,
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
            new_g = g + w
            if new_g < best_g.get(nb, float('inf')):
                best_g[nb] = new_g
                counter += 1
                generated += 1
                heapq.heappush(frontier, (new_g, counter, nb, path + [nb]))

    return None
