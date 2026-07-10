# Mảng (Array)

## 1. Khái niệm
Mảng (Array) là một cấu trúc dữ liệu tuyến tính lưu trữ một tập hợp các phần tử cùng kiểu dữ liệu tại các vị trí bộ nhớ liên tiếp nhau. Mỗi phần tử trong mảng được định danh bằng một chỉ số (index), bắt đầu từ 0.

## 2. Đặc điểm
- Kích thước có thể cố định (Static Array trong C/C++) hoặc linh hoạt (Dynamic Array như `list` trong Python, `std::vector` trong C++).
- Các phần tử nằm trên khối bộ nhớ liên tục.
- Cho phép truy cập trực tiếp phần tử ở bất kỳ chỉ số nào trong $O(1)$.

## 3. Độ phức tạp thuật toán
| Thao tác | Tốt nhất | Trung bình | Xấu nhất |
| :--- | :--- | :--- | :--- |
| **Truy cập (Access)** | $O(1)$ | $O(1)$ | $O(1)$ |
| **Tìm kiếm (Search)** | $O(1)$ | $O(n)$ | $O(n)$ |
| **Thêm (Insertion)** | $O(1)$ (cuối) | $O(n)$ | $O(n)$ |
| **Xóa (Deletion)** | $O(1)$ (cuối) | $O(n)$ | $O(n)$ |

## 4. Ưu và Nhược điểm
* **Ưu điểm**:
  * Tốc độ truy cập phần tử ngẫu nhiên cực nhanh nhờ công thức tính địa chỉ ô nhớ: `Địa chỉ phần tử i = Địa chỉ gốc + i * Kích thước phần tử`.
  * Tiết kiệm bộ nhớ hơn so với các cấu trúc dạng nút (Linked List) vì không cần lưu con trỏ liên kết.
* **Nhược điểm**:
  * Chi phí thêm/xóa phần tử ở giữa hoặc đầu mảng lớn ($O(n)$) do phải dời các phần tử còn lại.
  * Với mảng tĩnh, kích thước phải được khai báo trước và không thể thay đổi.

## 5. Ứng dụng thực tế
- Lưu trữ danh sách dữ liệu cố định hoặc biết trước kích thước.
- Làm nền tảng xây dựng các cấu trúc dữ liệu khác: Stack, Queue, Heap, Hash Table, Adjacency Matrix cho Graph.
- Bảng tra cứu (Lookup Tables) và thuật toán sắp xếp.
