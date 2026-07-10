"""
Heuristic functions cho các thuật toán tìm kiếm có thông tin.
Sử dụng công thức Haversine để tính khoảng cách đường chim bay
giữa hai điểm trên bề mặt Trái Đất dựa trên tọa độ GPS.
"""

import math


def haversine_distance(lat1, lng1, lat2, lng2):
    """
    Tính khoảng cách great-circle giữa hai điểm trên Trái Đất
    sử dụng công thức Haversine.
    
    Args:
        lat1, lng1: Tọa độ điểm 1 (độ)
        lat2, lng2: Tọa độ điểm 2 (độ)
    
    Returns:
        float: Khoảng cách tính bằng km
    """
    R = 6371  # Bán kính Trái Đất (km)

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(dlng / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return R * c
