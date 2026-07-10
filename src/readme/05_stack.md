# Ngăn xếp (Stack)

## 1. Khái niệm
Ngăn xếp (Stack) là một cấu trúc dữ liệu tuyến tính tuân theo nguyên lý **LIFO** (Last In, First Out - Vào sau, Ra trước). Phần tử được thêm vào sau cùng sẽ là phần tử đầu tiên được lấy ra.

## 2. Các thao tác cơ bản
- `push(item)`: Thêm một phần tử vào đỉnh (top) của Stack.
- `pop()`: Loại bỏ và trả về phần tử nằm ở đỉnh Stack.
- `peek()` / `top()`: Xem giá trị của phần tử ở đỉnh Stack mà không xóa nó.
- `is_empty()`: Kiểm tra Stack có rỗng hay không.
- `size()`: Lấy số lượng phần tử trong Stack.

## 3. Độ phức tạp thuật toán
| Thao tác | Độ phức tạp |
| :--- | :--- |
| **Push** | $O(1)$ |
| **Pop** | $O(1)$ |
| **Peek/Top** | $O(1)$ |
| **Search** | $O(n)$ |

## 4. Ưu và Nhược điểm
* **Ưu điểm**:
  * Các thao tác thêm và xóa ở đỉnh diễn ra cực kỳ nhanh ($O(1)$).
  * Kiểm soát dữ liệu theo đúng thứ tự đảo ngược rất tự nhiên.
* **Nhược điểm**:
  * Không thể truy cập ngẫu nhiên các phần tử ở giữa hoặc ở đáy Stack nếu không loại bỏ các phần tử bên trên.

## 5. Ứng dụng thực tế
- Quản lý bộ nhớ Stack (Call Stack) cho các lời gọi hàm đệ quy.
- Kiểm tra tính hợp lệ của dấu đóng/mở ngoặc trong trình biên dịch (`()`, `{}`, `[]`).
- Cài đặt tính năng Undo/Redo trong các phần mềm văn bản, đồ họa.
- Thuật toán duyệt đồ thị theo chiều sâu (DFS - Depth First Search).
- Chuyển đổi biểu thức số học (Infix $\rightarrow$ Postfix/Prefix).
