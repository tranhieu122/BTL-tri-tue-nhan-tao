"""
bfs.py – BFS (Breadth-First Search / Tìm kiếm theo chiều rộng)
  - Không dùng heuristic (tìm kiếm mù)
  - Đảm bảo tìm đường đi ít cạnh nhất, KHÔNG tối ưu về chi phí
"""

from collections import deque
from graph import get_neighbors


def bfs(graph, start, goal):
    """
    Chạy BFS từ start đến goal.

    Returns
    -------
    dict:
        path      – danh sách đỉnh trên đường đi
        cost      – tổng chi phí cạnh
        expanded  – số đỉnh mở rộng (được pop ra khỏi hàng đợi và xử lý)
        generated – số đỉnh sinh ra (được thêm vào hàng đợi)
        steps     – danh sách từng bước để in bảng chi tiết
    """
    queue = deque([(start, [start], 0)])
    visited = {start}
    expanded = 0
    generated = 1       # tính cả đỉnh khởi đầu
    steps = []

    while queue:
        node, path, cost = queue.popleft()
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

        for nb, w in get_neighbors(graph, node):
            if nb not in visited:
                visited.add(nb)
                generated += 1
                queue.append((nb, path + [nb], cost + w))

    return None
