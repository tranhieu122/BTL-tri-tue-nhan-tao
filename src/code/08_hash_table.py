"""
Minh họa Cấu trúc dữ liệu Bảng băm (Hash Table) tự cài đặt bằng phương pháp Separate Chaining trong Python
"""

class HashTable:
    """Bảng băm giải quyết đụng độ bằng Danh sách liên kết (Separate Chaining)."""
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(capacity)]

    def _hash(self, key) -> int:
        """Hàm băm đơn giản sử dụng hash() có sẵn của Python."""
        return abs(hash(key)) % self.capacity

    def put(self, key, value):
        """Thêm hoặc cập nhật cặp (Key, Value) - O(1) trung bình"""
        index = self._hash(key)
        bucket = self.table[index]
        
        # Kiểm tra xem key đã tồn tại chưa để cập nhật
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Nếu chưa có, thêm mới vào bucket
        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        """Lấy giá trị từ key - O(1) trung bình"""
        index = self._hash(key)
        bucket = self.table[index]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def remove(self, key) -> bool:
        """Xóa cặp (Key, Value) khỏi bảng băm - O(1) trung bình"""
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def display(self):
        """Hiển thị toàn bộ bảng băm."""
        print("--- Trạng thái Bảng Băm ---")
        for i, bucket in enumerate(self.table):
            print(f"Bucket [{i}]: {bucket}")


if __name__ == "__main__":
    ht = HashTable(capacity=5)
    print("--- Minh họa Bảng Băm (Hash Table) ---")
    ht.put("apple", 50)
    ht.put("banana", 30)
    ht.put("orange", 20)
    ht.put("grape", 40)
    ht.put("mango", 15)

    ht.display()

    print("\nLấy giá trị của 'banana':", ht.get("banana"))  # 30
    print("Lấy giá trị của 'watermelon':", ht.get("watermelon"))  # None

    print("\nXóa 'apple':", ht.remove("apple"))
    ht.display()
