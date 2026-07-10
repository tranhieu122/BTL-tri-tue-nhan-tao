# 🗺️ A* Pathfinding Visualization - Bản đồ Việt Nam

## Mô tả dự án

Ứng dụng web trực quan hóa các thuật toán tìm đường đi ngắn nhất trên bản đồ Việt Nam với **34 tỉnh thành**. Chương trình cho phép:

- Chọn điểm xuất phát và điểm đích trên bản đồ
- Đặt chướng ngại vật trên các tuyến đường
- Xem máy "suy nghĩ" từng bước (step-by-step visualization)
- So sánh hiệu suất giữa 6 thuật toán tìm kiếm

## 🧠 Thuật toán

### Tìm kiếm có thông tin (Informed Search)
| Thuật toán | Mô tả |
|-----------|-------|
| **A\*** | f(n) = g(n) + h(n), heuristic = Haversine distance |
| **Greedy Best-First** | Chỉ dùng h(n), nhanh nhưng không tối ưu |
| **Dijkstra** | Tìm đường ngắn nhất cổ điển |

### Tìm kiếm mù (Blind/Uninformed Search)
| Thuật toán | Mô tả |
|-----------|-------|
| **BFS** | Duyệt theo chiều rộng |
| **DFS** | Duyệt theo chiều sâu |
| **UCS** | Uniform Cost Search |

## 🛠️ Công nghệ

- **Backend**: Python, Flask, NetworkX, NumPy, SQLite
- **Frontend**: HTML5, CSS3, JavaScript (thuần)
- **Database**: SQLite3

## 🚀 Hướng dẫn chạy

### 1. Cài đặt dependencies

```bash
cd src/backend
pip install -r requirements.txt
```

### 2. Chạy Backend

```bash
cd src/backend
python app.py
```

Server sẽ chạy tại: `http://localhost:5000`

### 3. Mở Frontend

Mở file `src/frontend/index.html` bằng trình duyệt hoặc dùng Live Server.

## 📁 Cấu trúc thư mục

```
src/
├── backend/
│   ├── app.py                  # Flask API server
│   ├── requirements.txt
│   ├── algorithms/             # 6 thuật toán tìm kiếm
│   │   ├── astar.py
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── dijkstra.py
│   │   ├── greedy.py
│   │   ├── ucs.py
│   │   └── heuristics.py
│   ├── models/
│   │   └── graph_model.py      # NetworkX graph model
│   ├── database/
│   │   └── db.py               # SQLite database
│   └── data/
│       └── vietnam_cities.json  # Dữ liệu 34 tỉnh thành
│
└── frontend/
    ├── index.html              # Trang giao diện chính
    ├── css/
    │   ├── style.css           # Styles chính
    │   ├── map.css             # Styles bản đồ
    │   └── animations.css      # Animations
    └── js/
        ├── app.js              # Logic điều khiển chính
        ├── map.js              # Vẽ bản đồ SVG
        ├── algorithms.js       # Gọi API backend
        ├── visualization.js    # Trực quan hóa từng bước
        └── comparison.js       # So sánh thuật toán
```

## 👤 Tác giả

- **Trần Trung Hiếu**
- Đề tài: Xây dựng chương trình tìm đường đi ngắn nhất trên đồ thị bằng thuật toán A*
