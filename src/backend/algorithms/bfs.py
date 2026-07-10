"""
Thuật toán BFS (Breadth-First Search) - Tìm kiếm mù.
Duyệt đồ thị theo chiều rộng, không sử dụng heuristic.
Tìm được đường đi có ít cạnh nhất (không phải ngắn nhất theo trọng số).
"""

from collections import deque
import time


def bfs_search(graph, start, end, heuristic_func=None, blocked_edges=None):
    """
    Tìm đường đi bằng thuật toán BFS (tìm kiếm mù).
    
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

    # Queue: (node, path, cost)
    queue = deque([(start, [start], 0)])
    visited = set([start])
    exploration_steps = []

    while queue:
        current, path, cost = queue.popleft()

        # Ghi nhận bước thăm dò
        frontier_nodes = list(set(item[0] for item in queue))
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
                "algorithm": "BFS",
                "type": "blind",
                "path": path,
                "cost": round(cost, 2),
                "explored_count": len(visited),
                "exploration_steps": exploration_steps,
                "time_ms": round(elapsed, 4)
            }

        for neighbor, weight in graph.get(current, []):
            edge_key = frozenset({current, neighbor})
            if neighbor not in visited and edge_key not in blocked_edges:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], cost + weight))

    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "algorithm": "BFS",
        "type": "blind",
        "path": [],
        "cost": -1,
        "explored_count": len(visited),
        "exploration_steps": exploration_steps,
        "time_ms": round(elapsed, 4)
    }
