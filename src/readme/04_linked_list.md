# Danh sách liên kết (Linked List)

## 1. Khái niệm
Danh sách liên kết (Linked List) là một cấu trúc dữ liệu tuyến tính bao gồm chuỗi các phần tử gọi là các **Nút (Node)**. Khác với Mảng, các nút không cần nằm ở các ô nhớ liên tiếp nhau mà kết nối với nhau thông qua con trỏ (Pointer / Reference).

Mỗi Node gồm 2 thành phần chính:
- **Data**: Giá trị phần tử.
- **Next**: Con trỏ trỏ tới Node tiếp theo trong danh sách (và **Prev** trỏ tới Node phía trước nếu là Danh sách liên kết đôi).

## 2. Phân loại
1. **Danh sách liên kết đơn (Singly Linked List)**: Mỗi nút chỉ có 1 con trỏ `next`.
2. **Danh sách liên kết đôi (Doubly Linked List)**: Mỗi nút có 2 con trỏ `prev` và `next`.
3. **Danh sách liên kết vòng (Circular Linked List)**: Nút cuối cùng trỏ ngược lại nút đầu tiên.

## 3. Độ phức tạp thuật toán
| Thao tác | Đầu danh sách | Cuối danh sách | Vị trí bất kỳ ($k$) |
| :--- | :--- | :--- | :--- |
| **Truy cập (Access)** | $O(1)$ | $O(n)$ | $O(k)$ |
| **Tìm kiếm (Search)** | $O(n)$ | $O(n)$ | $O(n)$ |
| **Thêm (Insertion)** | $O(1)$ | $O(1)$ (nếu có con trỏ Tail) | $O(k)$ |
| **Xóa (Deletion)** | $O(1)$ | $O(n)$ ($O(1)$ với Doubly + Tail) | $O(k)$ |

## 4. Ưu và Nhược điểm
* **Ưu điểm**:
  * Kích thước động, dễ dàng mở rộng mà không cần cấp phát lại toàn bộ bộ nhớ.
  * Thêm/xóa phần tử ở đầu danh sách cực nhanh ($O(1)$).
* **Nhược điểm**:
  * Tốn thêm bộ nhớ để lưu các con trỏ (`next`, `prev`).
  * Không hỗ trợ truy cập ngẫu nhiên (Random Access); phải duyệt tuần tự từ đầu.

## 5. Ứng dụng thực tế
- Cài đặt Stack, Queue.
- Quản lý bộ nhớ đệm (LRU Cache).
- Lịch sử duyêt web (Back / Forward) dùng Doubly Linked List.
