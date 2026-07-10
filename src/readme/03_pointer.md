# Con trỏ (Pointer)

## 1. Khái niệm
Con trỏ (Pointer) là một biến đặc biệt dùng để lưu trữ địa chỉ ô nhớ của một biến khác thay vì lưu trữ giá trị trực tiếp. 

Con trỏ là khái niệm cốt lõi trong các ngôn ngữ lập trình hệ thống như C và C++. Trong Python, tất cả các biến đều hoạt động như một "tham chiếu đối tượng" (object reference) tương tự như con trỏ ẩn.

## 2. Các toán tử chính với Con trỏ trong C/C++
- Toán tử lấy địa chỉ `&`: Lấy địa chỉ bộ nhớ của biến.
- Toán tử giải tham chiếu `*`: Lấy giá trị nằm tại địa chỉ bộ nhớ mà con trỏ đang trỏ tới.

## 3. Các loại con trỏ
- **Null Pointer**: Con trỏ trỏ vào địa chỉ `0` hoặc `nullptr` (chưa trỏ vào đâu).
- **Dangling Pointer**: Con trỏ trỏ đến vùng nhớ đã bị giải phóng.
- **Void Pointer (Generic Pointer)**: Con trỏ không có kiểu dữ liệu xác định (`void*`).
- **Pointer to Pointer**: Con trỏ lưu địa chỉ của một con trỏ khác (`int**`).

## 4. Quản lý bộ nhớ động với Con trỏ (Heap Allocation)
- Trong C: `malloc()`, `calloc()`, `realloc()`, `free()`.
- Trong C++: `new`, `delete` hoặc các con trỏ thông minh (Smart Pointers: `std::unique_ptr`, `std::shared_ptr`).

## 5. Ưu và Nhược điểm
* **Ưu điểm**:
  * Quản lý và thao tác trực tiếp với bộ nhớ máy tính.
  * Giúp xây dựng các cấu trúc dữ liệu động (Danh sách liên kết, Cây, Đồ thị).
  * Truyền dữ liệu lớn vào hàm mà không cần sao chép (tối ưu hiệu năng).
* **Nhược điểm**:
  * Dễ gây ra lỗi rò rỉ bộ nhớ (Memory Leak) nếu không giải phóng đúng cách.
  * Nguy cơ lỗi truy cập ô nhớ không hợp lệ (Segmentation Fault / Access Violation).
