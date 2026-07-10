# Đống (Heap)

## 1. Khái niệm
Đống (Heap) là một cấu trúc dữ liệu dựa trên **Cây nhị phân hoàn chỉnh (Complete Binary Tree)** thỏa mãn tính chất Heap:
- **Max-Heap**: Giá trị của mỗi nút luôn **lớn hơn hoặc bằng** giá trị các nút con của nó. Phần tử lớn nhất nằm tại nút Gốc (Root).
- **Min-Heap**: Giá trị của mỗi nút luôn **nhỏ hơn hoặc bằng** giá trị các nút con của nó. Phần tử nhỏ nhất nằm tại nút Gốc (Root).

## 2. Biểu diễn Heap bằng Mảng (Array Representation)
Vì Heap là một cây nhị phân hoàn chỉnh, người ta thường biểu diễn Heap bằng một mảng liên tục thay vì dùng con trỏ để tiết kiệm bộ nhớ:
Cho nút tại chỉ số $i$ (bắt đầu từ index 0):
- **Chỉ số nút Cha (Parent)**: $\lfloor \frac{i - 1}{2} \rfloor$
- **Chỉ số nút Con trái (Left Child)**: $2i + 1$
- **Chỉ số nút Con phải (Right Child)**: $2i + 2$

## 3. Các thao tác chính
- `push(val)` / `insert(val)`: Thêm một phần tử vào Heap và thực hiện **Heapify-Up** để duy trì tính chất Heap.
- `pop()` / `extract_min(max)`: Lấy nút gốc ra khỏi Heap và thực hiện **Heapify-Down** để điều chỉnh lại cây.
- `heapify(array)`: Biến một mảng chưa sắp xếp thành một Heap trong thời gian $O(n)$.

## 4. Độ phức tạp thuật toán
| Thao tác | Độ phức tạp |
| :--- | :--- |
| **Lấy cực trị (Get Min/Max)** | $O(1)$ |
| **Thêm (Push)** | $O(\log n)$ |
| **Xóa cực trị (Pop)** | $O(\log n)$ |
| **Tạo Heap từ mảng (Heapify)** | $O(n)$ |
| **Sắp xếp Heap (Heap Sort)** | $O(n \log n)$ |

## 5. Ứng dụng thực tế
- Cài đặt Hàng đợi ưu tiên (Priority Queue).
- Thuật toán sắp xếp **Heap Sort**.
- Thuật toán Dijkstra tìm đường đi ngắn nhất.
- Tìm $k$ phần tử lớn nhất/nhỏ nhất trong dòng dữ liệu (Streaming Data / Top K Elements).
