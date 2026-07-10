# Cây nhị phân tìm kiếm (Binary Search Tree - BST)

## 1. Khái niệm
Cây nhị phân tìm kiếm (BST) là một dạng đặc biệt của Cây nhị phân, thỏa mãn tính chất sắp thứ tự sau với mọi nút $X$:
- Tất cả các nút thuộc cây con bên **trái** của $X$ đều có giá trị **nhỏ hơn** $X$.
- Tất cả các nút thuộc cây con bên **phải** của $X$ đều có giá trị **lớn hơn** $X$.
- Cây con bên trái và bên phải của $X$ cũng đều phải là Cây nhị phân tìm kiếm.

## 2. Các thao tác chính
- `search(val)`: Tìm kiếm một giá trị trên cây.
- `insert(val)`: Thêm một phần tử mới vào cây đúng vị trí thứ tự.
- `delete(val)`: Xóa một phần tử khỏi cây (xử lý 3 trường hợp: nút lá, nút có 1 con, nút có 2 con).
- `inorder_traversal()`: Duyệt cây In-order để thu được chuỗi các giá trị theo thứ tự tăng dần.

## 3. Độ phức tạp thuật toán
| Thao tác | Trung bình (Cây cân bằng) | Xấu nhất (Cây lệch phẳng) |
| :--- | :--- | :--- |
| **Tìm kiếm (Search)** | $O(\log n)$ | $O(n)$ |
| **Thêm (Insert)** | $O(\log n)$ | $O(n)$ |
| **Xóa (Delete)** | $O(\log n)$ | $O(n)$ |

*Lưu ý: Để tránh trường hợp xấu nhất $O(n)$ khi chèn dữ liệu theo thứ tự tăng/giảm dần, người ta sử dụng các cây tự cân bằng như AVL Tree hoặc Red-Black Tree.*

## 4. Ưu và Nhược điểm
* **Ưu điểm**:
  * Tốc độ tìm kiếm, chèn, xóa nhanh hơn mảng/danh sách liên kết thông thường.
  * Tự động duy trì thứ tự dữ liệu (In-order traversal trả về danh sách sắp xếp trong $O(n)$).
* **Nhược điểm**:
  * Có thể bị suy thoái thành dải phẳng (giống LinkedList) nếu không được cân bằng.

## 5. Ứng dụng thực tế
- Cài đặt danh sách tự sắp xếp (Self-balancing BST trong C++ `std::map`, `std::set`).
- Tìm kiếm phạm vi (Range Queries) và lưu trữ dữ liệu chỉ mục (Database Indexing).
