"""
graph.py – Định nghĩa đồ thị G1 và heuristic dùng chung cho tất cả thuật toán.
"""

# ── Đồ thị G1 ────────────────────────────────────────────────────────────────
# Danh sách kề: node → [(neighbor, edge_cost), ...]
G1_GRAPH = {
    'S': [('A', 2), ('B', 3)],
    'A': [('S', 2), ('B', 1), ('C', 3)],
    'B': [('S', 3), ('A', 1), ('D', 3)],
    'C': [('A', 3), ('D', 1), ('E', 3)],
    'D': [('B', 3), ('C', 1), ('F', 2)],
    'E': [('C', 3), ('G', 2)],
    'F': [('D', 2), ('G', 1)],
    'G': [('E', 2), ('F', 1)],
}

# Heuristic h(n): ước lượng chi phí từ n đến đích G
G1_HEURISTIC = {
    'S': 6.0, 'A': 4.0, 'B': 4.0, 'C': 4.0, 'D': 3.5,
    'E': 1.0, 'F': 1.0, 'G': 0.0,
}

G1_START = 'S'
G1_GOAL  = 'G'


def get_neighbors(graph, node):
    """Trả về danh sách đỉnh kề đã sắp xếp theo thứ tự alphabet."""
    return sorted(graph[node], key=lambda x: x[0])
