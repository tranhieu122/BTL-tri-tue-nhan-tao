"""
Minh họa Cấu trúc dữ liệu Hàng đợi (Queue) trong Python bằng collections.deque
"""

from collections import deque

class Queue:
    """Cài đặt Hàng đợi tối ưu với độ phức tạp O(1) cho cả enqueue và dequeue."""
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        """Thêm phần tử vào cuối hàng đợi - O(1)"""
        self._items.append(item)

    def dequeue(self):
        """Lấy phần tử ra khỏi đầu hàng đợi - O(1)"""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.popleft()

    def front(self):
        """Xem phần tử ở đầu hàng đợi - O(1)"""
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def __str__(self):
        return f"Queue(Front -> {list(self._items)} <- Rear)"


if __name__ == "__main__":
    print("--- Minh họa thao tác trên Hàng đợi (Queue) ---")
    q = Queue()
    q.enqueue("Khách hàng A")
    q.enqueue("Khách hàng B")
    q.enqueue("Khách hàng C")
    
    print("Trạng thái hàng đợi hiện tại:", q)
    print("Khách hàng đang phục vụ ở đầu hàng (front):", q.front())

    print("Phục vụ xong:", q.dequeue())  # Khách hàng A
    print("Trạng thái hàng đợi sau khi phục vụ:", q)

    q.enqueue("Khách hàng D")
    print("Thêm Khách hàng D vào cuối:", q)
