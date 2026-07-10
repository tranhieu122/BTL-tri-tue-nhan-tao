/*
  Minh họa Cấu trúc dữ liệu và Thao tác con trỏ trong C++
*/

#include <iostream>

void swapByPointer(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    std::cout << "=== Minh hoa Con tro (Pointer) trong C++ ===" << std::endl;

    int x = 42;
    int* ptr = &x; // ptr lưu địa chỉ ô nhớ của x

    std::cout << "Gia tri cua x: " << x << std::endl;
    std::cout << "Dia chi cua x (&x): " << &x << std::endl;
    std::cout << "Gia tri cua ptr (diachi): " << ptr << std::endl;
    std::cout << "Gia tri tai vi tri ptr tro toi (*ptr): " << *ptr << std::endl;

    // Thay đổi giá trị x thông qua con trỏ
    *ptr = 100;
    std::cout << "Sau khi hoan doi qua *ptr = 100, x = " << x << std::endl;

    // Hoán đổi giá trị bằng con trỏ
    int a = 5, b = 10;
    std::cout << "Truoc swap: a = " << a << ", b = " << b << std::endl;
    swapByPointer(&a, &b);
    std::cout << "Sau swapByPointer: a = " << a << ", b = " << b << std::endl;

    // Cấp phát bộ nhớ động trên Heap
    int* dynamicArr = new int[5]{10, 20, 30, 40, 50};
    std::cout << "Phan tu thu 2 trong mang dong (*(dynamicArr + 2)): " << *(dynamicArr + 2) << std::endl;

    // Giải phóng bộ nhớ
    delete[] dynamicArr;
    dynamicArr = nullptr;

    return 0;
}
