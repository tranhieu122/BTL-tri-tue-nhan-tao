"""
Thuật toán Dijkstra - Tìm kiếm có thông tin.
Tìm đường đi ngắn nhất từ nguồn đến đích trên đồ thị có trọng số.
Tương tự UCS nhưng thường được coi là thuật toán kinh điển riêng.
"""

import heapq
import time


def dijkstra_search(graph, start, end, heuristic_func=None, blocked_edges=None):
    """
    Tìm đường đi ngắn nhất bằng thuật toán Dijkstra.
    
    Args:
        graph: dict - {city: [(neighbor, distance), ...]}
        start: str - tên tỉnh xuất phát
        end: str - tên tỉnh đích
        heuristic_func: không sử dụng (giữ interface thống nhất)
        blocked_edges: set of frozenset - các cạnh bị chặn
    
    Returns:
        dict: kết quả tìm kiếm
    """
    if blocked_edges is None:
        blocked_edges = set()

    start_time = time.perf_counter()

    # Priority queue: (distance, counter, node, path)
    counter = 0
    open_list = [(0, counter, start, [start])]
    
    best_dist = {start: 0}
    visited = set()
    exploration_steps = []

    while open_list:
        dist, _, current, path = heapq.heappop(open_list)

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
            "current_cost": round(dist, 2)
        })

        if current == end:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "algorithm": "Dijkstra",
                "type": "uninformed",
                "path": path,
                "cost": round(dist, 2),
                "explored_count": len(visited),
                "exploration_steps": exploration_steps,
                "time_ms": round(elapsed, 4)
            }

        for neighbor, weight in graph.get(current, []):
            edge_key = frozenset({current, neighbor})
            if neighbor not in visited and edge_key not in blocked_edges:
                new_dist = dist + weight
                if neighbor not in best_dist or new_dist < best_dist[neighbor]:
                    best_dist[neighbor] = new_dist
                    counter += 1
                    heapq.heappush(
                        open_list,
                        (new_dist, counter, neighbor, path + [neighbor])
                    )

    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "algorithm": "Dijkstra",
        "type": "informed",
        "path": [],
        "cost": -1,
        "explored_count": len(visited),
        "exploration_steps": exploration_steps,
        "time_ms": round(elapsed, 4)
    }
