"""
Minh họa Cấu trúc dữ liệu Đồ thị (Graph) biểu diễn bằng Danh sách kề và thuật toán BFS, DFS trong Python
"""

from collections import deque

class Graph:
    """Đồ thị vô hướng biểu diễn bằng Danh sách kề (Adjacency List)."""
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex):
        """Thêm đỉnh vào đồ thị."""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, v1, v2):
        """Thêm cạnh vô hướng giữa v1 và v2."""
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.adj_list[v1].append(v2)
        self.adj_list[v2].append(v1)

    def bfs(self, start_vertex) -> list:
        """Duyệt đồ thị theo chiều rộng (BFS) sử dụng Queue - O(V + E)"""
        visited = set([start_vertex])
        queue = deque([start_vertex])
        result = []

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor in self.adj_list.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def dfs(self, start_vertex) -> list:
        """Duyệt đồ thị theo chiều sâu (DFS) sử dụng Stack - O(V + E)"""
        visited = set()
        result = []
        stack = [start_vertex]

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                # Đưa các đỉnh kề vào stack (đảo ngược để duyệt theo đúng thứ tự)
                for neighbor in reversed(self.adj_list.get(vertex, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return result

    def display(self):
        """In danh sách kề của đồ thị."""
        print("--- Danh sách kề Đồ thị ---")
        for vertex, neighbors in self.adj_list.items():
            print(f"{vertex} -> {neighbors}")


if __name__ == "__main__":
    g = Graph()
    edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('E', 'F')]
    for v1, v2 in edges:
        g.add_edge(v1, v2)

    g.display()

    print("\nDuyệt BFS từ đỉnh 'A':", g.bfs('A'))
    print("Duyệt DFS từ đỉnh 'A':", g.dfs('A'))
