"""
Minh họa Cấu trúc dữ liệu Chuỗi (String) và các thuật toán xử lý chuỗi cơ bản
"""

def is_palindrome(s: str) -> bool:
    """Kiểm tra chuỗi đối xứng bằng kỹ thuật hai con trỏ - O(n)"""
    left, right = 0, len(s) - 1
    while left < right:
        # Bỏ qua ký tự không phải chữ/số
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True

def naive_string_search(text: str, pattern: str) -> list:
    """Tìm kiếm chuỗi con đơn giản (Naive String Search) - O(N * M)"""
    n, m = len(text), len(pattern)
    positions = []
    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            positions.append(i)
    return positions

def string_operations_demo():
    print("--- Minh họa thao tác trên Chuỗi (String) ---")
    s = "Hello Artificial Intelligence"
    print("Chuỗi ban đầu:", s)
    print("Độ dài chuỗi:", len(s))
    print("Ký tự đầu tiên:", s[0])
    print("Ký tự cuối cùng:", s[-1])
    print("Đảo ngược chuỗi:", s[::-1])

    # Kiểm tra palindrome
    test_str = "A man, a plan, a canal: Panama"
    print(f"'{test_str}' có phải Palindrome không?", is_palindrome(test_str))

    # Tìm kiếm chuỗi con
    text = "ABAABADAABABA"
    pattern = "ABA"
    matches = naive_string_search(text, pattern)
    print(f"Vị trí xuất hiện của '{pattern}' trong '{text}':", matches)


if __name__ == "__main__":
    string_operations_demo()
