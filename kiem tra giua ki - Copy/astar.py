"""
astar.py – A* Search
  - Hàm đánh giá: f(n) = g(n) + h(n)
  - Tối ưu và đầy đủ khi h(n) là admissible (không đánh giá quá cao)
  - Mở rộng ít node hơn BFS/UCS nhờ hướng dẫn bởi heuristic
"""

import heapq
from graph import get_neighbors


def astar(graph, heuristic, start, goal):
    """
    Chạy A* từ start đến goal.
    Ưu tiên mở rộng đỉnh có f(n) = g(n) + h(n) nhỏ nhất.

    Parameters
    ----------
    heuristic : dict  –  h[node] = ước lượng chi phí từ node đến goal

    Returns
    -------
    dict: path, cost, expanded, generated, steps
    """
    counter = 0
    # (f, g, tie-breaker, node, path)
    frontier = [(heuristic[start], 0, counter, start, [start])]
    best_g = {start: 0}
    expanded = 0
    generated = 1
    steps = []

    while frontier:
        f, g, _, node, path = heapq.heappop(frontier)

        # Bỏ qua entry cũ nếu đã có đường tốt hơn
        if g > best_g.get(node, float('inf')):
            continue

        expanded += 1
        steps.append({
            'step': expanded,
            'node': node,
            'g': g,
            'h': heuristic[node],
            'f': round(f, 2),
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
                new_f = new_g + heuristic[nb]
                heapq.heappush(frontier,
                               (new_f, new_g, counter, nb, path + [nb]))

    return None
