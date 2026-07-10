# Chuỗi (String)

## 1. Khái niệm
Chuỗi (String) là một tập hợp các ký tự được lưu trữ theo thứ tự tuyến tính. Trong nhiều ngôn ngữ lập trình, chuỗi được coi là một mảng các ký tự (Array of Characters).

## 2. Đặc điểm
- Trong Python và Java, String là **Immutable** (không thể thay đổi trực tiếp nội dung sau khi khởi tạo). Mọi thao tác biến đổi chuỗi đều tạo ra một chuỗi mới.
- Trong C/C++, chuỗi có thể là **Mutable** (mảng ký tự kết thúc bằng ký tự null `\0`).
- Cho phép truy cập ký tự theo chỉ số trong $O(1)$.

## 3. Độ phức tạp thuật toán
| Thao tác | Độ phức tạp | Ghi chú |
| :--- | :--- | :--- |
| **Truy cập ký tự (Access)** | $O(1)$ | Theo vị trí chỉ số |
| **Tìm kiếm ký tự/chuỗi con** | $O(n)$ đến $O(n \times m)$ | Tùy thuật toán (Naive / KMP / Rabin-Karp) |
| **Nối chuỗi (Concatenation)** | $O(n + m)$ | Cần cấp phát bộ nhớ mới cho chuỗi kết quả |
| **So sánh chuỗi** | $O(\min(n, m))$ | So sánh từng ký tự từ đầu |

## 4. Các thuật toán xử lý chuỗi phổ biến
- **Knuth-Morris-Pratt (KMP)**: Tìm kiếm chuỗi con với thời gian $O(n + m)$.
- **Rabin-Karp**: Thuật toán tìm kiếm chuỗi con dựa trên hàm băm (Hash Function).
- **Z-algorithm** & **Manacher's Algorithm**: Tìm chuỗi đối xứng (Palindrome).

## 5. Ứng dụng thực tế
- Xử lý ngôn ngữ tự nhiên (NLP), phân tích cú pháp (Parsing).
- Công cụ tìm kiếm văn bản, biên dịch ngôn ngữ.
- Mã hóa và bảo mật dữ liệu (Cryptographic hashing, tokenizing).
