# Hàng đợi (Queue)

## 1. Khái niệm
Hàng đợi (Queue) là một cấu trúc dữ liệu tuyến tính tuân theo nguyên lý **FIFO** (First In, First Out - Vào trước, Ra trước). Phần tử được thêm vào đầu tiên sẽ là phần tử đầu tiên được lấy ra khỏi hàng đợi.

## 2. Các thao tác cơ bản
- `enqueue(item)`: Thêm một phần tử vào cuối (rear / back) của Queue.
- `dequeue()`: Loại bỏ và trả về phần tử nằm ở đầu (front) của Queue.
- `front()` / `peek()`: Xem giá trị của phần tử đầu Queue mà không xóa.
- `is_empty()`: Kiểm tra Queue có rỗng hay không.

## 3. Độ phức tạp thuật toán
| Thao tác | Độ phức tạp | Ghi chú |
| :--- | :--- | :--- |
| **Enqueue** | $O(1)$ | Thêm vào cuối hàng đợi |
| **Dequeue** | $O(1)$ | Sử dụng Doubly Linked List hoặc `collections.deque` |
| **Front/Peek** | $O(1)$ | Xem phần tử đầu |

*Lưu ý: Nếu cài đặt Queue bằng Mảng thông thường (Array), thao tác `dequeue` ở đầu mảng sẽ mất $O(n)$ do phải dời tất cả phần tử.*

## 4. Ưu và Nhược điểm
* **Ưu điểm**:
  * Đảm bảo tính công bằng theo thứ tự yêu cầu xử lý (First-Come, First-Served).
  * Thao tác thêm/xóa nhanh $O(1)$ khi được cài đặt đúng cách.
* **Nhược điểm**:
  * Không thể truy cập các phần tử ở giữa hàng đợi mà không lấy các phần tử phía trước ra.

## 5. Ứng dụng thực tế
- Quản lý hàng đợi tiến trình hệ điều hành (CPU Scheduling, Disk Scheduling).
- Bộ đệm IO (Input/Output Buffers), hàng đợi tin nhắn (Message Queue như RabbitMQ, Kafka).
- Hàng đợi yêu cầu trong các Web Server (handling HTTP Requests).
- Thuật toán duyệt đồ thị theo chiều rộng (BFS - Breadth First Search).
