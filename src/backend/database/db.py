"""
SQLite database module - Lưu trữ lịch sử tìm kiếm và dữ liệu đồ thị.
"""

import sqlite3
import os
import json
from datetime import datetime


class Database:
    """Quản lý kết nối và thao tác với SQLite database."""

    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(
                os.path.dirname(__file__), '..', 'data', 'vietnam_graph.db'
            )
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Tạo kết nối mới tới database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Khởi tạo các bảng trong database."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Bảng lưu thông tin tỉnh thành
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                lat REAL NOT NULL,
                lng REAL NOT NULL
            )
        ''')

        # Bảng lưu các cạnh (đường nối)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city1_id INTEGER NOT NULL,
                city2_id INTEGER NOT NULL,
                distance REAL NOT NULL,
                is_blocked INTEGER DEFAULT 0,
                FOREIGN KEY (city1_id) REFERENCES cities(id),
                FOREIGN KEY (city2_id) REFERENCES cities(id),
                UNIQUE(city1_id, city2_id)
            )
        ''')

        # Bảng lưu lịch sử tìm kiếm
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                algorithm TEXT NOT NULL,
                start_city TEXT NOT NULL,
                end_city TEXT NOT NULL,
                path TEXT,
                distance REAL,
                time_ms REAL,
                nodes_explored INTEGER,
                steps_count INTEGER,
                timestamp TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def load_cities_from_json(self, json_path):
        """Nạp dữ liệu tỉnh thành từ file JSON vào database (chỉ nạp nếu db trống)."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Kiểm tra xem bảng edges đã có dữ liệu chưa
        cursor.execute('SELECT COUNT(*) FROM edges')
        count = cursor.fetchone()[0]

        if count > 0:
            # Database đã có dữ liệu, không ghi đè để bảo toàn custom weights
            conn.close()
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        cursor.execute('DELETE FROM edges')
        cursor.execute('DELETE FROM cities')

        for city in data['cities']:
            cursor.execute(
                'INSERT OR REPLACE INTO cities (id, name, lat, lng) VALUES (?, ?, ?, ?)',
                (city['id'], city['name'], city['lat'], city['lng'])
            )

        for edge in data['edges']:
            cursor.execute(
                'INSERT OR REPLACE INTO edges (city1_id, city2_id, distance) VALUES (?, ?, ?)',
                (edge['from'], edge['to'], edge['distance'])
            )

        conn.commit()
        conn.close()

    def save_search_result(self, algorithm, start, end, path, distance, time_ms, nodes_explored, steps_count):
        """Lưu kết quả tìm kiếm vào lịch sử."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO search_history 
            (algorithm, start_city, end_city, path, distance, time_ms, nodes_explored, steps_count, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            algorithm, start, end,
            json.dumps(path, ensure_ascii=False),
            distance, time_ms, nodes_explored, steps_count,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def get_search_history(self, limit=50):
        """Lấy lịch sử tìm kiếm gần nhất."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM search_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_blocked_edges(self):
        """Lấy danh sách các cạnh bị chặn."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c1.name as city1, c2.name as city2
            FROM edges e
            JOIN cities c1 ON e.city1_id = c1.id
            JOIN cities c2 ON e.city2_id = c2.id
            WHERE e.is_blocked = 1
        ''')

        rows = cursor.fetchall()
        conn.close()

        return [(row['city1'], row['city2']) for row in rows]

    def get_all_edges(self):
        """Lấy danh sách tất cả các cạnh và trọng số."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c1.name as city1, c2.name as city2, e.distance, e.is_blocked
            FROM edges e
            JOIN cities c1 ON e.city1_id = c1.id
            JOIN cities c2 ON e.city2_id = c2.id
        ''')

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]


    def set_edge_blocked(self, city1_id, city2_id, blocked=True):
        """Đặt/gỡ chướng ngại vật trên một cạnh."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE edges SET is_blocked = ? 
            WHERE (city1_id = ? AND city2_id = ?) OR (city1_id = ? AND city2_id = ?)
        ''', (1 if blocked else 0, city1_id, city2_id, city2_id, city1_id))

        conn.commit()
        conn.close()

    def clear_all_blocks(self):
        """Gỡ tất cả chướng ngại vật."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE edges SET is_blocked = 0')
        conn.commit()
        conn.close()

    def update_edge_weight(self, city1_id, city2_id, new_weight):
        """Cập nhật trọng số của một cạnh."""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE edges SET distance = ? 
            WHERE (city1_id = ? AND city2_id = ?) OR (city1_id = ? AND city2_id = ?)
        ''', (new_weight, city1_id, city2_id, city2_id, city1_id))

        conn.commit()
        conn.close()

