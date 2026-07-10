"""
Thuật toán A* Search - Tìm kiếm có thông tin.
Sử dụng hàm đánh giá f(n) = g(n) + h(n)
  - g(n): chi phí thực tế từ start đến n
  - h(n): ước lượng chi phí từ n đến đích (heuristic)
Đảm bảo tìm được đường đi ngắn nhất nếu heuristic admissible.
"""

import heapq
import time


def astar_search(graph, start, end, heuristic_func, blocked_edges=None):
    """
    Tìm đường đi ngắn nhất bằng thuật toán A*.
    
    Args:
        graph: dict - {city: [(neighbor, distance), ...]}
        start: str - tên tỉnh xuất phát
        end: str - tên tỉnh đích
        heuristic_func: callable(city_name) -> float
        blocked_edges: set of frozenset - các cạnh bị chặn
    
    Returns:
        dict: kết quả tìm kiếm với path, cost, steps, v.v.
    """
    if blocked_edges is None:
        blocked_edges = set()

    start_time = time.perf_counter()

    # Priority queue: (f_cost, counter, node, path, g_cost)
    counter = 0
    h_start = heuristic_func(start)
    open_list = [(h_start, counter, start, [start], 0)]
    
    # Theo dõi g_cost tốt nhất cho mỗi node
    best_g = {start: 0}
    visited = set()
    exploration_steps = []

    while open_list:
        f_cost, _, current, path, g_cost = heapq.heappop(open_list)

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
            "current_cost": round(g_cost, 2),
            "f_cost": round(f_cost, 2)
        })

        # Tìm thấy đích
        if current == end:
            elapsed = (time.perf_counter() - start_time) * 1000
            return {
                "algorithm": "A*",
                "type": "informed",
                "path": path,
                "cost": round(g_cost, 2),
                "explored_count": len(visited),
                "exploration_steps": exploration_steps,
                "time_ms": round(elapsed, 4)
            }

        # Mở rộng các node kề
        for neighbor, weight in graph.get(current, []):
            edge_key = frozenset({current, neighbor})
            if neighbor not in visited and edge_key not in blocked_edges:
                new_g = g_cost + weight
                # Chỉ thêm nếu tìm được đường tốt hơn
                if neighbor not in best_g or new_g < best_g[neighbor]:
                    best_g[neighbor] = new_g
                    h = heuristic_func(neighbor)
                    new_f = new_g + h
                    counter += 1
                    heapq.heappush(
                        open_list,
                        (new_f, counter, neighbor, path + [neighbor], new_g)
                    )

    # Không tìm thấy đường
    elapsed = (time.perf_counter() - start_time) * 1000
    return {
        "algorithm": "A*",
        "type": "informed",
        "path": [],
        "cost": -1,
        "explored_count": len(visited),
        "exploration_steps": exploration_steps,
        "time_ms": round(elapsed, 4)
    }
