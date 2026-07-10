# Đồ thị (Graph)

## 1. Khái niệm
Đồ thị (Graph) là một cấu trúc dữ liệu phi tuyến tính bao gồm:
- Tập hợp các **Đỉnh (Vertices / Nodes)**, ký hiệu là $V$.
- Tập hợp các **Cạnh (Edges)** nối giữa các cặp đỉnh, ký hiệu là $E$.

Cú pháp tổng quát: $G = (V, E)$.

## 2. Phân loại Đồ thị
- **Đồ thị vô hướng (Undirected Graph)**: Các cạnh không có hướng (cạnh nối giữa A và B đi được cả 2 chiều).
- **Đồ thị có hướng (Directed Graph / Digraph)**: Mỗi cạnh chỉ đi từ đỉnh nguồn đến đỉnh đích ($A \rightarrow B$).
- **Đồ thị có trọng số (Weighted Graph)**: Mỗi cạnh được gán một chi phí/khoảng cách (weight).
- **Đồ thị không trọng số (Unweighted Graph)**: Chi phí giữa mọi cạnh coi như bằng 1.

## 3. Các phương pháp biểu diễn Đồ thị
1. **Danh sách kề (Adjacency List)**: Sử dụng Bảng băm hoặc Mảng danh sách để lưu các đỉnh kề của từng đỉnh. 
   - Không gian bộ nhớ: $O(V + E)$ (tối ưu cho đồ thị thưa).
2. **Ma trận kề (Adjacency Matrix)**: Sử dụng mảng 2 chiều kích thước $V \times V$.
   - Không gian bộ nhớ: $O(V^2)$ (tốt cho đồ thị dày).

## 4. Các thuật toán tìm kiếm và duyệt đồ thị cơ bản
- **Breadth-First Search (BFS)**: Duyệt theo chiều rộng, sử dụng **Queue**. Dùng tìm đường đi ngắn nhất trên đồ thị không trọng số.
- **Depth-First Search (DFS)**: Duyệt theo chiều sâu, sử dụng **Stack** hoặc **Đệ quy**.
- **Thuật toán A\*** & **Dijkstra**: Tìm đường đi ngắn nhất trên đồ thị có trọng số.

## 5. Độ phức tạp duyệt Đồ thị (BFS / DFS với Danh sách kề)
- Thời gian: $O(V + E)$
- Bộ nhớ: $O(V)$

## 6. Ứng dụng thực tế
- Mạng xã hội (Facebook, LinkedIn): Đỉnh là người dùng, Cạnh là quan hệ bạn bè.
- Bản đồ định vị chỉ đường (Google Maps): Đỉnh là giao lộ, Cạnh là tuyến đường với trọng số là khoảng cách/thời gian.
- Web Crawler: Đỉnh là trang web, Cạnh là các liên kết URL.
- Trí tuệ nhân tạo (AI Search & Pathfinding algorithms).
