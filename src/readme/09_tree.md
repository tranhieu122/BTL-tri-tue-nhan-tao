# Cây (Tree)

## 1. Khái niệm
Cây (Tree) là một cấu trúc dữ liệu phi tuyến tính (non-linear) dùng để biểu diễn dữ liệu dưới dạng phân cấp. Cây bao gồm các **Nút (Node)** được nối với nhau bằng các **Cạnh (Edge)**, bắt đầu từ một nút gốc duy nhất gọi là **Root**.

## 2. Các thuật ngữ quan trọng
- **Root (Nút gốc)**: Nút nằm ở đỉnh cao nhất của cây.
- **Parent / Child (Cha / Con)**: Nút cha trỏ đến nút con trực thuộc.
- **Leaf Node (Nút lá)**: Nút không có bất kỳ nút con nào.
- **Subtree (Cây con)**: Một nút cùng toàn bộ các nút con cháu của nó.
- **Depth (Độ sâu)**: Khoảng cách từ nút gốc đến nút hiện tại.
- **Height (Chiều cao)**: Khoảng cách đường đi dài nhất từ nút đó đến một nút lá.

## 3. Phân loại Cây
- **Cây tổng quát (General Tree)**: Mỗi nút có thể có số lượng nút con không hạn chế.
- **Cây nhị phân (Binary Tree)**: Mỗi nút có tối đa 2 nút con (Left Child và Right Child).
- **Cây N-ary (N-ary Tree)**: Mỗi nút có tối đa N nút con.

## 4. Các phương pháp duyệt Cây nhị phân (Traversals)
1. **Depth-First Search (DFS)**:
   - **In-order (Trai -> Goc -> Phai)**: Duyệt cây nhị phân tìm kiếm thu được danh sách đã sắp xếp.
   - **Pre-order (Goc -> Trai -> Phai)**: Dùng để sao chép cây hoặc tạo biểu thức Prefix.
   - **Post-order (Trai -> Phai -> Goc)**: Dùng để tính kích thước cây, xóa cây hoặc tạo biểu thức Postfix.
2. **Breadth-First Search (BFS / Level-order)**: Duyệt cây theo từng tầng từ trên xuống dưới, từ trái sang phải.

## 5. Ứng dụng thực tế
- Hệ thống tập tin và thư mục trên hệ điều hành.
- Cấu trúc cây DOM trong tài liệu HTML/XML.
- Cây cú pháp tự nhiên (Abstract Syntax Tree - AST) trong trình biên dịch.
