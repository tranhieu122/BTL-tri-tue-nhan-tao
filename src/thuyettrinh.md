# 📋 KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN (RÚT GỌN)
**Đề tài:** Tìm đường đi ngắn nhất bằng thuật toán A* trên bản đồ Việt Nam  
**Thời lượng:** 5 phút (9 Slides ngắn gọn)

---

## 🖥️ SLIDE 1: GIỚI THIỆU ĐỀ TÀI
* **Nội dung slide:**
  * Đề tài: Tìm đường đi ngắn nhất bằng thuật toán A* trên bản đồ Việt Nam (34 tỉnh thành).
  * Đối chứng: Dijkstra, BFS, DFS, UCS, Greedy.
  * SV thực hiện: Trần Trung Hiếu.
* **Lời thoại thuyết trình:**
  > *"Em chào thầy cô. Hôm nay em xin trình bày đồ án 'Tìm đường đi ngắn nhất bằng thuật toán A* và trực quan hóa trên bản đồ Việt Nam', đồng thời so sánh hiệu năng với 5 thuật toán tìm kiếm phổ biến khác."*

---

## 🖥️ SLIDE 2: MỤC TIÊU ĐỀ TÀI
* **Nội dung slide:**
  * **Ứng dụng:** Mô phỏng bài toán định vị, tối ưu lộ trình thực tế.
  * **Trực quan hóa:** Chạy hoạt ảnh từng bước loang của thuật toán trên bản đồ.
  * **Thực nghiệm:** Đo số liệu cụ thể để so sánh hiệu năng các thuật toán.
* **Lời thoại thuyết trình:**
  > *"Mục tiêu của đề tài là xây dựng một ứng dụng trực quan hóa sinh động quá trình tìm kiếm của máy, qua đó đưa ra số liệu thực nghiệm so sánh ưu, nhược điểm của từng thuật toán."*

---

## 🖥️ SLIDE 3: MÔ HÌNH HÓA ĐỒ THỊ
* **Nội dung slide:**
  * **Đỉnh (Nodes):** 34 tỉnh thành Việt Nam (tọa độ GPS thực tế).
  * **Cạnh (Edges):** Tuyến quốc lộ nối liền, trọng số là khoảng cách bộ (km).
  * **Cơ sở dữ liệu:** SQLite3 lưu chướng ngại vật và lịch sử tìm đường.
* **Lời thoại thuyết trình:**
  > *"Đồ thị gồm 34 đỉnh là 34 tỉnh thành với tọa độ GPS thật. Các cạnh nối có trọng số là khoảng cách đường bộ thực tế. Cơ sở dữ liệu SQLite3 hỗ trợ lưu trữ các tuyến đường bị chặn và lịch sử tìm kiếm."*

---

## 🖥️ SLIDE 4: THUẬT TOÁN TRỌNG TÂM A*
* **Nội dung slide:**
  * Công thức: **$f(n) = g(n) + h(n)$**
  * **$g(n)$**: Khoảng cách thực tế đã đi từ điểm xuất phát đến nút $n$.
  * **$h(n)$**: Khoảng cách ước lượng đường chim bay từ $n$ đến đích (Haversine x 0.6).
* **Lời thoại thuyết trình:**
  > *"A* sử dụng hàm đánh giá f(n) = g(n) + h(n). Trong đó g(n) là số km thực tế đã đi, còn h(n) là khoảng cách chim bay ước lượng đến đích bằng công thức Haversine nhân hệ số an toàn 0.6."*

---

## 🖥️ SLIDE 5: CÁC THUẬT TOÁN ĐỐI CHỨNG
* **Nội dung slide:**
  * **Tìm kiếm mù (Uninformed):**
    * *Dijkstra / UCS*: Loang tròn đều xung quanh, luôn tối ưu.
    * *BFS*: Tối ưu số cạnh đi qua.
    * *DFS*: Duyệt sâu ngẫu nhiên, không tối ưu.
  * **Tìm kiếm có thông tin (Informed):**
    * *Greedy Best-First*: Đi theo Heuristic h(n). Rất nhanh nhưng dễ đi vòng.
* **Lời thoại thuyết trình:**
  > *"Em cài đặt thêm UCS và Dijkstra đại diện cho tìm kiếm mù luôn tối ưu; BFS và DFS duyệt mù không tối ưu km; và Greedy Best-First duyệt chỉ theo Heuristic h(n) nhanh nhưng không đảm bảo đường ngắn nhất."*

---

## 🖥️ SLIDE 6: TỔNG QUAN KIẾN TRÚC HỆ THỐNG
* **Nội dung slide:**
  * **Mô hình:** Client - Server.
  * **Frontend:** HTML5, CSS3 (Glassmorphism), Vanilla JS (Fetch API). Bản đồ vẽ dạng SVG tương tác.
  * **Backend:** Python Flask API, đồ thị NetworkX, cơ sở dữ liệu SQLite3.
* **Lời thoại thuyết trình:**
  > *"Hệ thống chạy trên mô hình Client-Server. Frontend dùng JS và SVG để vẽ bản đồ tương tác và chạy hoạt ảnh. Backend dùng Flask và NetworkX xử lý đồ thị trong bộ nhớ, lưu dữ liệu vào SQLite3."*

---

## 🖥️ SLIDE 7: CÁC TÍNH NĂNG CHÍNH
* **Nội dung slide:**
  * Click chọn điểm xuất phát/đích trực tiếp trên bản đồ.
  * Chạy hoạt ảnh màu hiển thị nút đang xét, hàng đợi và nút đã duyệt.
  * Bật/tắt chướng ngại vật (chặn đường) và sửa khoảng cách trực tiếp.
* **Lời thoại thuyết trình:**
  > *"Người dùng có thể chọn điểm đi/đích bằng cách click lên bản đồ, xem hoạt ảnh máy duyệt tìm đường theo thời gian thực, đồng thời có thể click chặn đường hoặc sửa số km."*

---

## 🖥️ SLIDE 8: KẾT QUẢ SO SÁNH HIỆU SUẤT
* **Nội dung slide:**
  * **Tối ưu:** A*, Dijkstra, UCS luôn cho đường đi ngắn nhất giống nhau.
  * **Số node duyệt:** A* giảm 30% - 50% số node cần duyệt so với Dijkstra nhờ Heuristic.
  * **Greedy:** Duyệt cực ít node nhưng đường đi không tối ưu.
* **Lời thoại thuyết trình:**
  > *"Kết quả thực nghiệm chỉ ra A*, Dijkstra và UCS luôn tìm được đường ngắn nhất. Tuy nhiên, nhờ Heuristic định hướng, A* giảm được 30% đến 50% số node cần duyệt so với Dijkstra."*

---

## 🖥️ SLIDE 9: KẾT LUẬN & HƯỚNG PHÁT TRIỂN
* **Nội dung slide:**
  * **Đạt được:** Trực quan hóa tìm đường mượt mà, chứng minh thực nghiệm lý thuyết AI.
  * **Phát triển:** Mở rộng lên 63 tỉnh thành, tích hợp API bản đồ thương mại thời gian thực.
* **Lời thoại thuyết trình:**
  > *"Đồ án đã hoàn thành mục tiêu trực quan hóa và so sánh thuật toán sinh động. Hướng phát triển tiếp theo là mở rộng đồ thị lên 63 tỉnh thành Việt Nam. Em xin cảm ơn thầy cô đã lắng nghe."*
