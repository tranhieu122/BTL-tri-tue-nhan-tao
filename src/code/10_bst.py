"""
Minh họa Cấu trúc dữ liệu Cây nhị phân tìm kiếm (Binary Search Tree - BST) trong Python
"""

class BSTNode:
    """Nút trên cây BST."""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BinarySearchTree:
    """Cấu trúc Cây nhị phân tìm kiếm."""
    def __init__(self):
        self.root = None

    def insert(self, val):
        """Thêm phần tử vào BST - O(log n) trung bình"""
        if not self.root:
            self.root = BSTNode(val)
        else:
            self._insert_recursive(self.root, val)

    def _insert_recursive(self, node, val):
        if val < node.val:
            if not node.left:
                node.left = BSTNode(val)
            else:
                self._insert_recursive(node.left, val)
        elif val > node.val:
            if not node.right:
                node.right = BSTNode(val)
            else:
                self._insert_recursive(node.right, val)

    def search(self, val) -> bool:
        """Tìm kiếm giá trị trên BST - O(log n) trung bình"""
        return self._search_recursive(self.root, val)

    def _search_recursive(self, node, val) -> bool:
        if not node:
            return False
        if node.val == val:
            return True
        if val < node.val:
            return self._search_recursive(node.left, val)
        return self._search_recursive(node.right, val)

    def delete(self, val):
        """Xóa giá trị khỏi BST - O(log n) trung bình"""
        self.root = self._delete_recursive(self.root, val)

    def _delete_recursive(self, node, val):
        if not node:
            return None
        if val < node.val:
            node.left = self._delete_recursive(node.left, val)
        elif val > node.val:
            node.right = self._delete_recursive(node.right, val)
        else:
            # TH1: Nút lá hoặc chỉ có 1 con
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # TH2: Nút có cả 2 con -> Tìm nút nhỏ nhất bên cây con phải (In-order successor)
            min_node = self._find_min(node.right)
            node.val = min_node.val
            node.right = self._delete_recursive(node.right, min_node.val)
        return node

    def _find_min(self, node):
        curr = node
        while curr.left:
            curr = curr.left
        return curr

    def inorder(self) -> list:
        """Duyệt In-order thu được mảng đã sắp xếp."""
        res = []
        self._inorder_recursive(self.root, res)
        return res

    def _inorder_recursive(self, node, res):
        if node:
            self._inorder_recursive(node.left, res)
            res.append(node.val)
            self._inorder_recursive(node.right, res)


if __name__ == "__main__":
    bst = BinarySearchTree()
    print("--- Minh họa Cây nhị phân tìm kiếm (BST) ---")
    values = [50, 30, 70, 20, 40, 60, 80]
    for v in values:
        bst.insert(v)

    print("Duyệt In-order (Tự động sắp xếp):", bst.inorder())  # [20, 30, 40, 50, 60, 70, 80]
    print("Tìm giá trị 40:", bst.search(40))  # True
    print("Tìm giá trị 90:", bst.search(90))  # False

    print("\nXóa nút 30 (nút có 2 con):")
    bst.delete(30)
    print("Duyệt In-order sau khi xóa 30:", bst.inorder())
