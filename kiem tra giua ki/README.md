# Báo cáo thực nghiệm thuật toán tìm kiếm trên đồ thị G1

## a) Biểu diễn đồ thị

Đồ thị được biểu diễn dưới dạng danh sách kề có trọng số (weighted adjacency list), cài đặt bằng kiểu `dict` trong Python. Mỗi đỉnh ánh xạ tới một danh sách các cặp `(đỉnh_kề, trọng_số_cạnh)`.

Cách biểu diễn này phù hợp cho các thuật toán tìm kiếm vì:
- Truy xuất láng giềng nhanh theo từng đỉnh.
- Dễ lưu trọng số cạnh để tính `g(n)` cho UCS và A*.
- Dễ tái sử dụng chung cho BFS, DFS, IDS, Best-First/UCS, GBFS, A*.

### Hình đồ thị G1

![Đồ thị G1](Hình%20G1.png)

### Định nghĩa đồ thị và heuristic

```python
# graph.py

graph = {
    'S': [('A', 2), ('B', 3)],
    'A': [('S', 2), ('B', 1), ('C', 3)],
    'B': [('S', 3), ('A', 1), ('D', 3)],
    'C': [('A', 3), ('D', 1), ('E', 3)],
    'D': [('B', 3), ('C', 1), ('F', 2)],
    'E': [('C', 3), ('G', 2)],
    'F': [('D', 2), ('G', 1)],
    'G': [('E', 2), ('F', 1)],
}

h = {
    'S': 6.0,
    'A': 4.0,
    'B': 4.0,
    'C': 4.0,
    'D': 3.5,
    'E': 1.0,
    'F': 1.0,
    'G': 0.0,
}
```

Lưu ý: Trong mã nguồn hiện tại, hai biến này được đặt tên là `G1_GRAPH` và `G1_HEURISTIC` trong file `graph.py`, nội dung tương đương đoạn trên.

---

## b) Cấu trúc dữ liệu điều khiển frontier của từng thuật toán

Frontier là tập các trạng thái/đỉnh sẽ được xét tiếp theo. Mỗi thuật toán khác nhau ở cách tổ chức frontier:

- DFS: dùng Stack (LIFO) hoặc đệ quy, đi sâu trước.
- BFS: dùng Queue (FIFO), đi theo từng lớp.
- IDS: dùng DFS có giới hạn độ sâu, sau đó tăng dần giới hạn (`0, 1, 2, ...`) và chạy lại.
- UCS / Best-First (trong bài này): dùng Priority Queue (`heapq`), ưu tiên nhỏ nhất theo `g(n)`.
- GBFS: dùng Priority Queue (`heapq`), ưu tiên nhỏ nhất theo `h(n)`.
- A*: dùng Priority Queue (`heapq`), ưu tiên nhỏ nhất theo `f(n) = g(n) + h(n)`.

Tóm tắt hàm ưu tiên:
- UCS/Best-First: `priority = g(n)`
- GBFS: `priority = h(n)`
- A*: `priority = g(n) + h(n)`

---

## c) Cách đo thời gian thực thi

Phần đo thời gian dùng `time.perf_counter()` thay vì `time.time()` vì `perf_counter()` có độ phân giải cao hơn và ổn định hơn cho benchmark ngắn.

Quy trình đo:
1. Chạy mỗi thuật toán 20 lần liên tiếp trên cùng một đồ thị G1.
2. Với mỗi lần chạy, ghi lại `t_end - t_start` bằng `perf_counter()`.
3. Tính thời gian trung bình (đơn vị ms) để đưa vào bảng so sánh.
4. (Tùy chọn nâng cao) có thể tính thêm độ lệch chuẩn để đánh giá độ ổn định.

Ví dụ:

```python
import time

times = []
for _ in range(20):
    t0 = time.perf_counter()
    result = algorithm()
    t1 = time.perf_counter()
    times.append(t1 - t0)

avg_ms = (sum(times) / 20) * 1000
```

Điểm quan trọng cần nêu rõ trong báo cáo:

Vì đồ thị đầu vào là cố định, nên đường đi, chi phí, số node mở rộng (expanded) và số node sinh (generated) không đổi qua 20 lần chạy. Chỉ thời gian thực thi là đại lượng cần lặp nhiều lần và lấy trung bình để so sánh.

---

## Tệp liên quan trong project

- `graph.py`: định nghĩa đồ thị và heuristic.
- `bfs.py`, `dfs.py`, `ids.py`, `best_first.py`, `gbfs.py`, `astar.py`: cài đặt thuật toán.
- `main.py`: chạy và in chi tiết kết quả từng thuật toán.
- `benchmark.py`: đo benchmark 20 lần và xuất `result.csv`.
- `result.csv`: bảng kết quả tổng hợp.
