"""
Thuật toán UCS (Uniform Cost Search) - Tìm kiếm mù.
Mở rộng node có chi phí đường đi thấp nhất.
Tương tự Dijkstra, nhưng được phân loại là tìm kiếm mù
vì không sử dụng heuristic.
Đảm bảo tìm được đường đi ngắn nhất.
"""

import heapq
import time


def ucs_search(graph, start, end, heuristic_func=None, blocked_edges=None):
    """
    Tìm đường đi bằng thuật toán Uniform Cost Search (tìm kiếm mù).
    
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

    # Priority queue: (cost, counter, node, path)
    counter = 0
    open_list = [(0, counter, start, [start])]
    
    best_cost = {start: 0}
    visited = set()
    exploration_steps = []

    while open_list:
        cost, _, current, path = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)

        # Ghi nhận bước thăm dò
        frontier_nodes = list(set(
            item[2] for item in open_list if item[2] not in visited
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
                "algorithm": "UCS",
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
                new_cost = cost + weight
                if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                    best_cost[neighbor] = new_cost
                    counter += 1
                    heapq.heappush(
                        open_list,
                        (new_cost, counter, neighbor, path + [neighbor])
                    )

    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "algorithm": "UCS",
        "type": "blind",
        "path": [],
        "cost": -1,
        "explored_count": len(visited),
        "exploration_steps": exploration_steps,
        "time_ms": round(elapsed, 4)
    }
