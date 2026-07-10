"""
Minh họa Cấu trúc dữ liệu Danh sách liên kết đơn (Singly Linked List) trong Python
"""

class Node:
    """Nút đại diện cho 1 phần tử trong danh sách liên kết."""
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """Cấu trúc Danh sách liên kết đơn."""
    def __init__(self):
        self.head = None

    def prepend(self, data):
        """Thêm nút vào đầu danh sách - O(1)"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def append(self, data):
        """Thêm nút vào cuối danh sách - O(n)"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def delete(self, key):
        """Xóa nút có giá trị bằng key - O(n)"""
        curr = self.head
        
        # Nếu nút đầu tiên chứa key
        if curr and curr.data == key:
            self.head = curr.next
            return True
        
        prev = None
        while curr and curr.data != key:
            prev = curr
            curr = curr.next
            
        if not curr:
            return False  # Không tìm thấy
            
        prev.next = curr.next
        return True

    def search(self, key):
        """Tìm kiếm xem key có tồn tại hay không - O(n)"""
        curr = self.head
        while curr:
            if curr.data == key:
                return True
            curr = curr.next
        return False

    def reverse(self):
        """Đảo ngược danh sách liên kết - O(n)"""
        prev = None
        curr = self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    def display(self):
        """In toàn bộ danh sách liên kết."""
        elements = []
        curr = self.head
        while curr:
            elements.append(str(curr.data))
            curr = curr.next
        print(" -> ".join(elements) + " -> None")


if __name__ == "__main__":
    ll = SinglyLinkedList()
    print("--- Minh họa Danh sách liên kết đơn ---")
    ll.append(10)
    ll.append(20)
    ll.append(30)
    ll.prepend(5)
    
    print("Danh sách hiện tại:")
    ll.display()  # 5 -> 10 -> 20 -> 30 -> None

    print("Tìm 20 trong danh sách:", ll.search(20))  # True
    
    print("Xóa phần tử 10:")
    ll.delete(10)
    ll.display()  # 5 -> 20 -> 30 -> None

    print("Đảo ngược danh sách:")
    ll.reverse()
    ll.display()  # 30 -> 20 -> 5 -> None
