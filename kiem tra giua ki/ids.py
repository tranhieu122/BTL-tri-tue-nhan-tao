"""
ids.py – IDS (Iterative Deepening Search / Tìm kiếm sâu dần)
  - Không dùng heuristic (tìm kiếm mù)
  - Kết hợp ưu điểm BFS (tối ưu số cạnh) và DFS (ít bộ nhớ)
  - Lặp lại DFS với giới hạn độ sâu tăng dần
"""

from graph import get_neighbors


def ids(graph, start, goal, max_depth=20):
    """
    Chạy IDS từ start đến goal.

    Returns
    -------
    dict: path, cost, expanded, generated, steps_by_depth, depth_found
    """
    total_expanded = 0
    total_generated = 0
    steps_by_depth = {}

    def dls(node, goal, limit, path, cost, steps):
        """Depth-Limited Search (DLS) – DFS với giới hạn độ sâu."""
        nonlocal total_expanded, total_generated

        total_expanded += 1
        steps.append({
            'step': total_expanded,
            'node': node,
            'depth': len(path) - 1,
            'path': '→'.join(path),
            'cost': cost,
            'note': 'Goal!' if node == goal else '',
        })

        if node == goal:
            return path, cost

        if limit == 0:
            return None

        for nb, w in get_neighbors(graph, node):
            if nb not in path:          # tránh chu trình
                total_generated += 1
                result = dls(nb, goal, limit - 1, path + [nb], cost + w, steps)
                if result is not None:
                    return result

        return None

    for depth in range(0, max_depth + 1):
        steps = []
        total_generated += 1            # đỉnh khởi đầu mỗi vòng lặp
        result = dls(start, goal, depth, [start], 0, steps)
        steps_by_depth[depth] = steps

        if result is not None:
            path, cost = result
            return {
                'path': path, 'cost': cost,
                'expanded': total_expanded, 'generated': total_generated,
                'steps_by_depth': steps_by_depth,
                'depth_found': depth,
            }

    return None
