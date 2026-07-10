Build, explain, debug, or extend shortest-path / pathfinding programs using the A* (A-star) algorithm on graphs, grids, or maps. Use this skill whenever the user asks about A*, shortest path, pathfinding, route finding, heuristic search, grid/maze navigation, GPS-style routing, or NPC/game AI movement — even if they don't say "A*" by name (e.g. "find the fastest route between two points", "make my character navigate around obstacles", "compare Dijkstra vs A*"). Also use when the user wants a working Python implementation, wants to adapt A* to a new graph representation (grid, weighted graph, road network), or wants a heuristic function designed for their specific problem.A* Pathfinding Skill
Hướng dẫn Claude xây dựng, giải thích, hoặc mở rộng chương trình tìm đường đi ngắn nhất bằng thuật toán A*.
Khi nào dùng skill này

Người dùng hỏi về thuật toán A*, tìm đường đi ngắn nhất, pathfinding, định tuyến bản đồ/GPS
Người dùng muốn cài đặt A* cho: đồ thị có trọng số, lưới ô vuông (grid/maze), bản đồ có tọa độ
Người dùng muốn so sánh A* với Dijkstra, BFS, hoặc Greedy Best-First Search
Người dùng cần chọn/thiết kế heuristic phù hợp với bài toán của họ (game AI, robot, mạng lưới, v.v.)

Kiến thức cốt lõi
A* chọn node để mở rộng dựa trên: f(n) = g(n) + h(n)
Ký hiệuÝ nghĩag(n)Chi phí thực đã đi từ start đến nh(n)Chi phí ước lượng (heuristic) từ n đến đíchf(n)Tổng ước lượng — dùng để sắp xếp thứ tự mở rộng node
Điều kiện heuristic phải thỏa (admissible): không bao giờ ước lượng cao hơn chi phí thật còn lại, nếu không kết quả có thể không tối ưu.
Chọn heuristic theo bài toán
Loại di chuyểnHeuristic phù hợpTự do mọi hướng (bản đồ, tọa độ thực)Euclidean: sqrt(dx² + dy²)Lưới ô vuông, chỉ đi ngang/dọcManhattan: `Lưới ô vuông, cho phép đi chéoChebyshev: `max(Không có tọa độ / đồ thị trừu tượngh(n) = 0 (A* suy biến thành Dijkstra)
Cấu trúc dữ liệu cần dùng khi cài đặt

open_set: min-heap (heapq) chứa (f_score, node), luôn lấy node có f nhỏ nhất
g_score: dict lưu chi phí thực từ start đến từng node
came_from: dict lưu node cha để truy vết đường đi
visited: tập node đã xử lý xong, tránh xử lý lặp

Các bước triển khai

Biểu diễn đồ thị bằng danh sách kề (adjacency list); nếu cần heuristic theo khoảng cách, lưu thêm tọa độ (x, y) từng node
Khởi tạo open_set với node start, g_score[start] = 0
Lặp: lấy node có f(n) nhỏ nhất khỏi open_set

Nếu là đích → dừng, truy vết đường đi qua came_from
Ngược lại, duyệt các node kề, cập nhật g_score/came_from nếu tìm được đường tốt hơn, đẩy vào open_set


Nếu open_set cạn mà chưa tới đích → không có đường đi

Script có sẵn
File scripts/a_star.py chứa cài đặt đầy đủ, chạy được ngay:

Class Graph (thêm node có tọa độ, thêm cạnh, heuristic Euclid tự động)
Hàm a_star(graph, start, goal) trả về (đường_đi, tổng_chi_phí)
Có ví dụ mẫu chạy trực tiếp qua python3 scripts/a_star.py

Khi người dùng cần một bản A* làm việc ngay, hãy dùng lại file này làm nền, rồi tùy biến theo:

Đổi hàm heuristic() nếu bài toán là lưới ô vuông (Manhattan/Chebyshev) thay vì Euclid
Đổi add_edge/add_node nếu input đến từ file (CSV, JSON, ma trận) thay vì khai báo tay
Thêm giới hạn vật cản (obstacle) nếu là bài toán grid/maze — chỉ cần bỏ qua các ô bị chặn khi liệt kê neighbor

Các lỗi thường gặp cần tránh khi giải thích/code cho người dùng

Heuristic vượt quá chi phí thật → mất tính tối ưu (không còn là A* đúng nghĩa)
Quên kiểm tra visited trước khi xử lý lại node → tốn thời gian, có thể lặp vô hạn nếu đồ thị có chu trình âm (lưu ý: A* không hỗ trợ trọng số âm)
Nhầm lẫn g(n) với f(n) khi so sánh trong heap
Không xử lý trường hợp không có đường đi (open_set rỗng)

Cách trình bày kết quả cho người dùng

Nếu người dùng chỉ hỏi lý thuyết → giải thích công thức, cấu trúc dữ liệu, các bước, không cần viết code
Nếu người dùng muốn chương trình chạy được → tạo file .py hoàn chỉnh, chạy thử để xác nhận đúng trước khi đưa ra
Nếu người dùng có bài toán cụ thể (grid, bản đồ thật, game) → hỏi rõ: dữ liệu đầu vào là gì (tọa độ? ma trận? file?), có vật cản không, di chuyển ngang/dọc/chéo — rồi tùy biến scripts/a_star.py cho phù hợp thay vì viết lại từ đầu