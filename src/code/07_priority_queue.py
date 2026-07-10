"""
Minh họa Cấu trúc dữ liệu Hàng đợi ưu tiên (Priority Queue) bằng thư viện heapq trong Python
"""

import heapq

class PriorityQueue:
    """Cài đặt Hàng đợi ưu tiên (Min-Priority Queue)."""
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        """
        Thêm phần tử vào PQ kèm độ ưu tiên.
        Độ ưu tiên nhỏ hơn = Ưu tiên cao hơn.
        """
        # Sử dụng tuple (priority, index, item) để xử lý trường hợp cùng priority
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        """Lấy phần tử có độ ưu tiên cao nhất - O(log n)"""
        if self.is_empty():
            raise IndexError("Pop from empty priority queue")
        return heapq.heappop(self._queue)[-1]

    def peek(self):
        """Xem phần tử có độ ưu tiên cao nhất - O(1)"""
        if self.is_empty():
            return None
        return self._queue[0][-1]

    def is_empty(self) -> bool:
        return len(self._queue) == 0


if __name__ == "__main__":
    print("--- Minh họa Hàng đợi ưu tiên (Priority Queue) ---")
    pq = PriorityQueue()

    # Thêm nhiệm vụ với mức độ ưu tiên (số nhỏ hơn = ưu tiên hơn)
    pq.push("Nhiệm vụ thông thường A", priority=3)
    pq.push("Cấp cứu hệ thống B", priority=1)
    pq.push("Nhiệm vụ quan trọng C", priority=2)
    pq.push("Nhiệm vụ ưu tiên cực cao D", priority=1)

    print("Nhiệm vụ ưu tiên cao nhất hiện tại:", pq.peek())

    print("\nXử lý các nhiệm vụ theo thứ tự ưu tiên:")
    while not pq.is_empty():
        task = pq.pop()
        print(" -> Đang xử lý:", task)
