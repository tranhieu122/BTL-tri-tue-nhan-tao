"""
Mô phỏng cơ chế làm việc của Con trỏ (Pointer) và Địa chỉ ô nhớ trong Python
"""

class SimulatedMemory:
    """Mô phỏng bộ nhớ máy tính để minh họa khái niệm địa chỉ ô nhớ và con trỏ."""
    def __init__(self, size=16):
        self.memory = [0] * size
        self.allocated = [False] * size

    def allocate(self, value):
        """Cấp phát 1 ô nhớ cho giá trị value và trả về địa chỉ ô nhớ."""
        for addr in range(len(self.memory)):
            if not self.allocated[addr]:
                self.allocated[addr] = True
                self.memory[addr] = value
                return addr
        raise MemoryError("Out of simulated memory")

    def free(self, address):
        """Giải phóng ô nhớ tại địa chỉ address."""
        if 0 <= address < len(self.memory):
            self.allocated[address] = False
            self.memory[address] = 0

    def dereference(self, address):
        """Giải tham chiếu (nhận giá trị từ địa chỉ ô nhớ) - Tương đương toán tử *ptr"""
        if 0 <= address < len(self.memory) and self.allocated[address]:
            return self.memory[address]
        raise ValueError(f"Segmentation Fault: Invalid memory access at address {address}")

    def write(self, address, value):
        """Ghi giá trị vào ô nhớ - Tương đương *ptr = val"""
        if 0 <= address < len(self.memory) and self.allocated[address]:
            self.memory[address] = value
        else:
            raise ValueError(f"Segmentation Fault: Cannot write to address {address}")


if __name__ == "__main__":
    ram = SimulatedMemory(size=8)

    print("=== Mô phỏng Con trỏ trong Python ===")
    # 1. Cấp phát biến x = 42
    addr_x = ram.allocate(42)
    print(f"Biến x lưu giá trị 42 tại địa chỉ ô nhớ: 0x{addr_x:02X}")

    # 2. Con trỏ ptr trỏ tới x (ptr = &x)
    ptr = addr_x
    print(f"Con trỏ ptr lưu địa chỉ: 0x{ptr:02X}")

    # 3. Lấy giá trị qua giải tham chiếu (*ptr)
    print("Giá trị tại *ptr:", ram.dereference(ptr))

    # 4. Thay đổi giá trị qua con trỏ (*ptr = 99)
    ram.write(ptr, 99)
    print("Sau khi gán *ptr = 99, giá trị x là:", ram.dereference(addr_x))

    # 5. Giải phóng bộ nhớ
    ram.free(addr_x)
    print("Đã free(addr_x).")
