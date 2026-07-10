"""
Minh họa Cấu trúc dữ liệu Ngăn xếp (Stack) và ứng dụng kiểm tra ngoặc hợp lệ trong Python
"""

class Stack:
    """Cài đặt Stack bằng danh sách động (List)."""
    def __init__(self):
        self._items = []

    def push(self, item):
        """Thêm phần tử vào đỉnh Stack - O(1)"""
        self._items.append(item)

    def pop(self):
        """Lấy phần tử khỏi đỉnh Stack - O(1)"""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Xem phần tử ở đỉnh Stack - O(1)"""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """Kiểm tra Stack rỗng."""
        return len(self._items) == 0

    def size( int) -> int:
        return len(self._items)

    def __str__(self):
        return f"Stack(Top -> {self._items[::-1]})"


def is_valid_parentheses(s: str) -> bool:
    """Ứng dụng Stack: Kiểm tra chuỗi ngoặc hợp lệ - O(n)"""
    stack = Stack()
    bracket_map = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in bracket_map.values():
            stack.push(char)
        elif char in bracket_map.keys():
            if stack.is_empty() or stack.pop() != bracket_map[char]:
                return False

    return stack.is_empty()


if __name__ == "__main__":
    print("--- Minh họa thao tác với Ngăn xếp (Stack) ---")
    st = Stack()
    st.push(10)
    st.push(20)
    st.push(30)
    print("Stack sau khi push 10, 20, 30:", st)
    print("Phần tử ở đỉnh (peek):", st.peek())

    print("Pop phần tử:", st.pop())  # 30
    print("Stack còn lại:", st)

    print("\n--- Ứng dụng: Kiểm tra dấu ngoặc hợp lệ ---")
    expr1 = "{[()()]}"
    expr2 = "{[(])}"
    print(f"Chuỗi '{expr1}' hợp lệ?", is_valid_parentheses(expr1))  # True
    print(f"Chuỗi '{expr2}' hợp lệ?", is_valid_parentheses(expr2))  # False
