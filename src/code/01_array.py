"""
Minh họa Cấu trúc dữ liệu Mảng (Array / Dynamic Array) trong Python
"""

class CustomArray:
    """Cấu trúc dữ liệu Mảng tĩnh đơn giản tự cài đặt."""
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.data = [None] * capacity

    def get(self, index):
        """Truy cập phần tử theo chỉ số - O(1)"""
        if 0 <= index < self.size:
            return self.data[index]
        raise IndexError("Index out of range")

    def insert(self, index, val):
        """Thêm phần tử vào vị trí bất kỳ - O(n)"""
        if self.size >= self.capacity:
            raise OverflowError("Array is full")
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")
        
        # Dời các phần tử sang phải
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
            
        self.data[index] = val
        self.size += 1

    def append(self, val):
        """Thêm vào cuối mảng - O(1)"""
        self.insert(self.size, val)

    def delete(self, index):
        """Xóa phần tử tại vị trí index - O(n)"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        
        removed_val = self.data[index]
        # Dời các phần tử sang trái
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
            
        self.data[self.size - 1] = None
        self.size -= 1
        return removed_val

    def search(self, val):
        """Tìm kiếm tuyến tính - O(n)"""
        for i in range(self.size):
            if self.data[i] == val:
                return i
        return -1

    def __str__(self):
        return str([self.data[i] for i in range(self.size)])


if __name__ == "__main__":
    arr = CustomArray(capacity=5)
    print("--- Minh họa thao tác trên Mảng ---")
    arr.append(10)
    arr.append(20)
    arr.append(30)
    print("Mảng ban đầu:", arr)  # [10, 20, 30]

    arr.insert(1, 15)
    print("Sau khi chèn 15 vào index 1:", arr)  # [10, 15, 20, 30]

    print("Phần tử tại index 2:", arr.get(2))  # 20
    print("Tìm vị trí của 30:", arr.search(30))  # 3

    arr.delete(1)
    print("Sau khi xóa tại index 1:", arr)  # [10, 20, 30]
