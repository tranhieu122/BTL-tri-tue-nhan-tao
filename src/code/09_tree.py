"""
Minh họa Cấu trúc dữ liệu Cây nhị phân (Binary Tree) và các thuật toán duyệt cây trong Python
"""

from collections import deque

class TreeNode:
    """Nút đại diện cho 1 phần tử trên Cây nhị phân."""
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def preorder_traversal(root, result=None):
    """Duyệt Pre-order: Root -> Left -> Right"""
    if result is None:
        result = []
    if root:
        result.append(root.val)
        preorder_traversal(root.left, result)
        preorder_traversal(root.right, result)
    return result


def inorder_traversal(root, result=None):
    """Duyệt In-order: Left -> Root -> Right"""
    if result is None:
        result = []
    if root:
        inorder_traversal(root.left, result)
        result.append(root.val)
        inorder_traversal(root.right, result)
    return result


def postorder_traversal(root, result=None):
    """Duyệt Post-order: Left -> Right -> Root"""
    if result is None:
        result = []
    if root:
        postorder_traversal(root.left, result)
        postorder_traversal(root.right, result)
        result.append(root.val)
    return result


def level_order_traversal(root):
    """Duyệt BFS theo từng tầng (Level-order)"""
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


if __name__ == "__main__":
    """
            1
           / \
          2   3
         / \
        4   5
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    print("--- Minh họa Duyệt Cây nhị phân ---")
    print("Pre-order (Root -> Left -> Right):", preorder_traversal(root))  # [1, 2, 4, 5, 3]
    print("In-order (Left -> Root -> Right):", inorder_traversal(root))    # [4, 2, 5, 1, 3]
    print("Post-order (Left -> Right -> Root):", postorder_traversal(root))  # [4, 5, 2, 3, 1]
    print("Level-order (BFS theo tầng):", level_order_traversal(root))     # [1, 2, 3, 4, 5]
