"""
Thuật toán Greedy Best-First Search - Tìm kiếm có thông tin.
Chỉ sử dụng hàm heuristic h(n) để chọn node mở rộng tiếp theo.
Nhanh nhưng KHÔNG đảm bảo tìm được đường đi ngắn nhất.
"""

import heapq
import time


def greedy_search(graph, start, end, heuristic_func, blocked_edges=None):
    """
    Tìm đường đi bằng thuật toán Greedy Best-First Search.
    
    Args:
        graph: dict - {city: [(neighbor, distance), ...]}
        start: str - tên tỉnh xuất phát
        end: str - tên tỉnh đích
        heuristic_func: callable(city_name) -> float
        blocked_edges: set of frozenset - các cạnh bị chặn
    
    Returns:
        dict: kết quả tìm kiếm
    """
    if blocked_edges is None:
        blocked_edges = set()

    start_time = time.perf_counter()

    # Priority queue: (h_cost, counter, node, path, actual_cost)
    counter = 0
    h_start = heuristic_func(start)
    open_list = [(h_start, counter, start, [start], 0)]
    
    visited = set()
    exploration_steps = []

    while open_list:
        h_cost, _, current, path, actual_cost = heapq.heappop(open_list)

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
            "current_cost": round(actual_cost, 2),
            "h_cost": round(h_cost, 2)
        })

        if current == end:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "algorithm": "Greedy",
                "type": "informed",
                "path": path,
                "cost": round(actual_cost, 2),
                "explored_count": len(visited),
                "exploration_steps": exploration_steps,
                "time_ms": round(elapsed, 4)
            }

        for neighbor, weight in graph.get(current, []):
            edge_key = frozenset({current, neighbor})
            if neighbor not in visited and edge_key not in blocked_edges:
                h = heuristic_func(neighbor)
                counter += 1
                heapq.heappush(
                    open_list,
                    (h, counter, neighbor, path + [neighbor], actual_cost + weight)
                )

    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "algorithm": "Greedy",
        "type": "informed",
        "path": [],
        "cost": -1,
        "explored_count": len(visited),
        "exploration_steps": exploration_steps,
        "time_ms": round(elapsed, 4)
    }
