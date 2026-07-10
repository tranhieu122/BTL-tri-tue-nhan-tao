# Hàng đợi ưu tiên (Priority Queue)

## 1. Khái niệm
Hàng đợi ưu tiên (Priority Queue) là một dạng mở rộng của Hàng đợi (Queue), trong đó mỗi phần tử đi kèm với một **độ ưu tiên (priority)**. Phần tử có độ ưu tiên cao nhất sẽ luôn luôn được phục vụ/lấy ra trước, bất kể thời điểm nó được thêm vào hàng đợi.

## 2. Cách cài đặt phổ biến
- **Cấu trúc đống (Binary Heap)**: Cài đặt phổ biến và tối ưu nhất (Min-Heap hoặc Max-Heap).
- **Mảng/Danh sách chưa sắp xếp**: Thêm $O(1)$, lấy phần tử ưu tiên $O(n)$.
- **Mảng/Danh sách đã sắp xếp**: Thêm $O(n)$, lấy phần tử ưu tiên $O(1)$.

## 3. Độ phức tạp thuật toán (Sử dụng Binary Heap)
| Thao tác | Độ phức tạp |
| :--- | :--- |
| **Thêm phần tử (Enqueue / Push)** | $O(\log n)$ |
| **Lấy phần tử ưu tiên nhất (Dequeue / Pop)** | $O(\log n)$ |
| **Xem phần tử ưu tiên nhất (Peek / Top)** | $O(1)$ |

## 4. Ưu và Nhược điểm
* **Ưu điểm**:
  * Tự động duy trì phần tử có độ ưu tiên cao nhất ở vị trí đầu tiên.
  * Hiệu năng cao ($O(\log n)$) với cấu trúc Binary Heap.
* **Nhược điểm**:
  * Việc truy cập phần tử bất kỳ có độ ưu tiên trung bình tốn chi phí $O(n)$.

## 5. Ứng dụng thực tế
- Thuật toán tìm đường đi ngắn nhất **Dijkstra** và thuật toán **A***.
- Lập lịch tiến trình ưu tiên trong Hệ điều hành (CPU Task Scheduler).
- Mã hóa dữ liệu Huffman (Huffman Coding trong nén file).
- Quản lý sự kiện trong mô phỏng hệ thống (Discrete Event Simulation).
