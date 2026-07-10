"""
Minh họa Cấu trúc dữ liệu Min-Heap tự cài đặt bằng Mảng trong Python
"""

class MinHeap:
    """Cài đặt Min-Heap dựa trên mảng 1 chiều."""
    def __init__(self):
        self.heap = []

    def _parent(self, i) -> int:
        return (i - 1) // 2

    def _left_child(self, i) -> int:
        return 2 * i + 1

    def _right_child(self, i) -> int:
        return 2 * i + 2

    def push(self, val):
        """Thêm phần tử vào Min-Heap - O(log n)"""
        self.heap.append(val)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i):
        """Đẩy phần tử lên trên nếu nhỏ hơn nút cha."""
        while i > 0 and self.heap[i] < self.heap[self._parent(i)]:
            p = self._parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def pop(self):
        """Lấy giá trị nhỏ nhất (nút gốc) ra khỏi Heap - O(log n)"""
        if not self.heap:
            raise IndexError("Pop from empty heap")
        if len(self.heap) == 1:
            return self.heap.pop()

        root_val = self.heap[0]
        # Đưa phần tử cuối mảng lên làm nút gốc
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root_val

    def _heapify_down(self, i):
        """Hạ phần tử xuống dưới nếu lớn hơn nút con."""
        smallest = i
        left = self._left_child(i)
        right = self._right_child(i)

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self._heapify_down(smallest)

    def peek(self):
        """Xem giá trị nhỏ nhất - O(1)"""
        return self.heap[0] if self.heap else None

    def __str__(self):
        return str(self.heap)


if __name__ == "__main__":
    heap = MinHeap()
    print("--- Minh họa Min-Heap ---")
    data = [15, 10, 20, 5, 8, 30]
    print("Thêm các phần tử:", data)
    for val in data:
        heap.push(val)

    print("Mảng biểu diễn Min-Heap:", heap)
    print("Phần tử nhỏ nhất (Root):", heap.peek())  # 5

    print("\nLấy các phần tử ra theo thứ tự tăng dần (Heap Sort):")
    sorted_res = []
    while heap.heap:
        sorted_res.append(heap.pop())
    print("Kết quả đã sắp xếp:", sorted_res)  # [5, 8, 10, 15, 20, 30]
