"""
Thuật toán DFS (Depth-First Search) - Tìm kiếm mù.
Duyệt đồ thị theo chiều sâu, không sử dụng heuristic.
Tìm được MỘT đường đi (không đảm bảo ngắn nhất).
"""

import time


def dfs_search(graph, start, end, heuristic_func=None, blocked_edges=None):
    """
    Tìm đường đi bằng thuật toán DFS (tìm kiếm mù).
    
    Args:
        graph: dict - {city: [(neighbor, distance), ...]}
        start: str - tên tỉnh xuất phát
        end: str - tên tỉnh đích
        heuristic_func: không sử dụng (tìm kiếm mù)
        blocked_edges: set of frozenset - các cạnh bị chặn
    
    Returns:
        dict: kết quả tìm kiếm
    """
    if blocked_edges is None:
        blocked_edges = set()

    start_time = time.perf_counter()

    # Stack: (node, path, cost)
    stack = [(start, [start], 0)]
    visited = set()
    exploration_steps = []

    while stack:
        current, path, cost = stack.pop()

        if current in visited:
            continue

        visited.add(current)

        # Ghi nhận bước thăm dò
        frontier_nodes = list(set(
            item[0] for item in stack if item[0] not in visited
        ))
        exploration_steps.append({
            "step": len(exploration_steps) + 1,
            "current": current,
            "frontier": frontier_nodes,
            "visited": list(visited),
            "current_path": list(path),
            "current_cost": round(cost, 2)
        })

        if current == end:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "algorithm": "DFS",
                "type": "blind",
                "path": path,
                "cost": round(cost, 2),
                "explored_count": len(visited),
                "exploration_steps": exploration_steps,
                "time_ms": round(elapsed, 4)
            }

        # Thêm các neighbor vào stack (đảo thứ tự để duyệt theo alphabet)
        neighbors = sorted(graph.get(current, []), key=lambda x: x[0], reverse=True)
        for neighbor, weight in neighbors:
            edge_key = frozenset({current, neighbor})
            if neighbor not in visited and edge_key not in blocked_edges:
                stack.append((neighbor, path + [neighbor], cost + weight))

    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "algorithm": "DFS",
        "type": "blind",
        "path": [],
        "cost": -1,
        "explored_count": len(visited),
        "exploration_steps": exploration_steps,
        "time_ms": round(elapsed, 4)
    }
