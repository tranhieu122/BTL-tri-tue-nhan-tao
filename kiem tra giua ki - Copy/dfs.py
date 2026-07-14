"""
dfs.py – DFS (Depth-First Search / Tìm kiếm theo chiều sâu)
  - Không dùng heuristic (tìm kiếm mù)
  - Không đảm bảo đường đi tối ưu
"""

from graph import get_neighbors


def dfs(graph, start, goal):
    """
    Chạy DFS từ start đến goal (dùng stack, tránh lặp đỉnh đã thăm).

    Returns
    -------
    dict: path, cost, expanded, generated, steps
    """
    # Đẩy ngược để xử lý theo thứ tự alphabet (A trước B)
    stack = [(start, [start], 0)]
    visited = set()
    expanded = 0
    generated = 1
    steps = []

    while stack:
        node, path, cost = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        expanded += 1
        steps.append({
            'step': expanded,
            'node': node,
            'path': '→'.join(path),
            'cost': cost,
            'note': 'Goal!' if node == goal else '',
        })

        if node == goal:
            return {
                'path': path, 'cost': cost,
                'expanded': expanded, 'generated': generated,
                'steps': steps,
            }

        # Đẩy ngược để đỉnh alphabet nhỏ hơn được pop trước
        for nb, w in reversed(get_neighbors(graph, node)):
            if nb not in visited:
                generated += 1
                stack.append((nb, path + [nb], cost + w))

    return None
