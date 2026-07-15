"""
Graph model sử dụng NetworkX - Quản lý đồ thị Việt Nam.
"""

import json
import os
import networkx as nx


class VietnamGraph:
    """
    Đồ thị Việt Nam sau sắp xếp 2025.
    Sử dụng NetworkX để quản lý cấu trúc đồ thị.
    """

    def __init__(self):
        self.G = nx.Graph()
        self.cities = {}
        self.metadata = {}
        self.blocked_edges = set()
        self._load_data()

    def _load_data(self):
        """Nạp dữ liệu từ file JSON."""
        data_path = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'vietnam_cities.json'
        )
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.metadata = data.get('metadata', {})

        # Thêm các node (đơn vị hành chính / đặc khu)
        for city in data['cities']:
            self.G.add_node(
                city['name'],
                lat=city['lat'],
                lng=city['lng'],
                id=city['id'],
                type=city.get('type', 'province'),
                region=city.get('region', 'Unknown')
            )
            self.cities[city['name']] = {
                'lat': city['lat'],
                'lng': city['lng'],
                'id': city['id'],
                'type': city.get('type', 'province'),
                'region': city.get('region', 'Unknown')
            }

        # Thêm các edge (đường nối) - dùng id để tìm tên
        city_id_map = {c['id']: c['name'] for c in data['cities']}
        for edge in data['edges']:
            from_city = city_id_map[edge['from']]
            to_city = city_id_map[edge['to']]
            self.G.add_edge(from_city, to_city, weight=edge['distance'])

    def get_adjacency(self, additional_blocked_edges=None):
        """
        Trả về danh sách kề dưới dạng dict.
        Bỏ qua các cạnh đang bị chặn (chướng ngại vật).
        
        Returns:
            dict: {city_name: [(neighbor_name, distance), ...]}
        """
        blocked_edges = self.blocked_edges | set(additional_blocked_edges or ())
        adj = {}
        for node in self.G.nodes():
            adj[node] = []
            for neighbor in self.G.neighbors(node):
                edge_key = frozenset({node, neighbor})
                if edge_key not in blocked_edges:
                    weight = self.G[node][neighbor]['weight']
                    adj[node].append((neighbor, weight))
        return adj

    def block_edge(self, city1, city2):
        """Đặt chướng ngại vật trên cạnh."""
        self.blocked_edges.add(frozenset({city1, city2}))

    def unblock_edge(self, city1, city2):
        """Gỡ chướng ngại vật trên cạnh."""
        self.blocked_edges.discard(frozenset({city1, city2}))

    def clear_all_blocks(self):
        """Gỡ tất cả chướng ngại vật."""
        self.blocked_edges.clear()

    def is_blocked(self, city1, city2):
        """Kiểm tra cạnh có bị chặn không."""
        return frozenset({city1, city2}) in self.blocked_edges

    def get_coords(self, city_name):
        """Lấy tọa độ GPS của tỉnh thành."""
        city = self.cities.get(city_name)
        if city:
            return city['lat'], city['lng']
        return None

    def get_city_id(self, city_name):
        """Lấy ID của tỉnh thành."""
        city = self.cities.get(city_name)
        if city:
            return city['id']
        return None

    def get_all_data(self):
        """
        Trả về toàn bộ dữ liệu đồ thị cho frontend.
        
        Returns:
            dict: {nodes: [...], edges: [...]}
        """
        nodes = []
        for name, data in self.cities.items():
            nodes.append({
                'name': name,
                'lat': data['lat'],
                'lng': data['lng'],
                'id': data['id'],
                'type': data.get('type', 'province'),
                'region': data.get('region', 'Unknown')
            })

        edges = []
        for u, v, data in self.G.edges(data=True):
            edge_key = frozenset({u, v})
            edges.append({
                'from': u,
                'to': v,
                'distance': data['weight'],
                'blocked': edge_key in self.blocked_edges
            })

        return {
            'metadata': self.metadata,
            'nodes': nodes,
            'edges': edges
        }

    def get_city_names(self):
        """Trả về danh sách tên tất cả tỉnh thành."""
        return list(self.cities.keys())

    def update_edge_weight(self, city1, city2, new_weight):
        """Cập nhật trọng số của một cạnh trong đồ thị."""
        if self.G.has_edge(city1, city2):
            self.G[city1][city2]['weight'] = new_weight
            return True
        return False

    def has_edge(self, city1, city2):
        """Kiểm tra hai tỉnh thành có tuyến đường trực tiếp hay không."""
        return self.G.has_edge(city1, city2)

