# Bảng băm (Hash Table)

## 1. Khái niệm
Bảng băm (Hash Table / Hash Map) là một cấu trúc dữ liệu lưu trữ dữ liệu dưới dạng cặp **Khóa - Giá trị (Key - Value)**. Bảng băm sử dụng một **Hàm băm (Hash Function)** để chuyển đổi một khóa thành chỉ số mảng (index), từ đó giúp truy xuất dữ liệu cực kỳ nhanh chóng.

## 2. Giải quyết đụng độ băm (Hash Collision)
Khi 2 khóa khác nhau tạo ra cùng 1 chỉ số băm, đụng độ sẽ xảy ra. Các phương pháp giải quyết chính:
1. **Separating Chaining (Liên kết chuỗi)**: Mỗi vị trí trong bảng chứa một Danh sách liên kết (Linked List) hoặc cây nhỏ để lưu các phần tử bị đụng độ.
2. **Open Addressing (Dò địa chỉ mở)**:
   - **Linear Probing**: Tìm ô trống tiếp theo tuyến tính $(i + 1, i + 2, \dots)$.
   - **Quadratic Probing**: Tìm ô trống theo bình phương $(i + 1^2, i + 2^2, \dots)$.
   - **Double Hashing**: Dùng hàm băm thứ hai để tính khoảng dời.

## 3. Độ phức tạp thuật toán
| Thao tác | Trung bình | Xấu nhất |
| :--- | :--- | :--- |
| **Tìm kiếm (Search)** | $O(1)$ | $O(n)$ (khi đụng độ toàn bộ) |
| **Thêm (Insert)** | $O(1)$ | $O(n)$ |
| **Xóa (Delete)** | $O(1)$ | $O(n)$ |

## 4. Ưu và Nhược điểm
* **Ưu điểm**:
  * Tốc độ tìm kiếm, thêm, xóa cực nhanh ($O(1)$ trung bình).
  * Tra cứu dữ liệu bằng khóa có ý nghĩa (string, object ID,...) thay vì chỉ số nguyên.
* **Nhược điểm**:
  * Dữ liệu trong bảng băm không tự động sắp xếp theo thứ tự.
  * Hiệu năng suy giảm nếu hàm băm kém (gây ra quá nhiều đụng độ).

## 5. Ứng dụng thực tế
- Cài đặt `dict` trong Python, `std::unordered_map` trong C++, `HashMap` trong Java.
- Hệ thống Caching dữ liệu (Redis, Memcached).
- Kiểm tra tính duy nhất (Unique values / Set data structure).
- Bộ đếm tần suất xuất hiện của các phần tử.
