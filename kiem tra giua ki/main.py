import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Tắt cảnh báo log chia cho 0 trong một số epoch đầu tiên
warnings.filterwarnings('ignore')

# Hàm phụ trợ dùng để vẽ và hiển thị biểu đồ
def plot_epoch(train_data, test_data, title, filename, epochs):
    plt.figure(figsize=(10, 6))
    
    plt.plot(range(1, epochs + 1), train_data, 
             label=f'Huấn luyện (Train) - Cuối: {train_data[-1]*100:.1f}%', 
             linewidth=2.5, marker='o', markersize=4, color='#1f77b4') 
    plt.plot(range(1, epochs + 1), test_data, 
             label=f'Kiểm tra (Test) - Cuối: {test_data[-1]*100:.1f}%', 
             linewidth=2.5, marker='s', markersize=4, color='#d62728')  
    
    plt.title(title, fontsize=15, fontweight='bold', pad=15)
    plt.ylabel('Độ chính xác (Accuracy)', fontsize=12, fontweight='bold')
    plt.xlabel('Vòng lặp (Epoch)', fontsize=12, fontweight='bold')
    
    plt.legend(loc='lower right', fontsize=11, frameon=True, shadow=True)
    plt.xticks(np.arange(0, epochs + 1, 5))
    
    best_test = max(test_data)
    plt.axhline(y=best_test, color='gray', linestyle='--', alpha=0.7)
    plt.text(2, best_test + 0.01, f'Max Test: {best_test*100:.1f}%', color='red', fontsize=10, fontweight='bold')
    
    plt.grid(True, which='major', linestyle='-', alpha=0.5)
    plt.minorticks_on()
    plt.grid(True, which='minor', linestyle=':', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show(block=False)  # Giúp vẽ đồ thị ra ngay lập tức
    plt.pause(0.5)         # Tạm nghỉ xíu để đồ thị kịp hiện lên trên Colab
    print(f"\n[+] Đã vẽ và lưu xong: {filename}!")

def main():
    print("======================================================================")
    print(" BÀI KIỂM TRA: PHÂN LOẠI HOA IRIS - NAIVE BAYES (CÓ BIỂU ĐỒ EPOCH)")
    print("======================================================================")
    
    # 1. Tải và chia dữ liệu
    iris = load_iris()
    X = iris.data
    y = iris.target
    target_names = iris.target_names
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=1/3, random_state=42, stratify=y
    )
    
    # 2. Huấn luyện qua các Epochs để thu thập dữ liệu vẽ biểu đồ
    print("\n[+] Đang mô phỏng quá trình huấn luyện qua các Epochs...")
    nb_classifier = GaussianNB()
    classes = np.unique(y)
    
    # Chuẩn bị danh sách lưu trữ độ chính xác
    train_acc = []
    test_acc = []
    train_acc_classes = {0: [], 1: [], 2: []} # 0: setosa, 1: versicolor, 2: virginica
    test_acc_classes = {0: [], 1: [], 2: []}
    epochs = 45 
    
    np.random.seed(42)
    for epoch in range(1, epochs + 1):
        sample_size = max(5, int(epoch * 2.2))
        idx = np.random.choice(len(X_train), size=sample_size, replace=False)
        X_batch = X_train[idx]
        y_batch = y_train[idx]
        
        nb_classifier.partial_fit(X_batch, y_batch, classes=classes)
        
        y_train_pred = nb_classifier.predict(X_train)
        y_test_pred = nb_classifier.predict(X_test)
        
        # Độ chính xác chung
        train_acc.append(accuracy_score(y_train, y_train_pred))
        test_acc.append(accuracy_score(y_test, y_test_pred))
        
        # Độ chính xác của riêng từng loài hoa
        for i in range(3):
            mask_tr = (y_train == i)
            if np.sum(mask_tr) > 0:
                train_acc_classes[i].append(accuracy_score(y_train[mask_tr], y_train_pred[mask_tr]))
            else:
                train_acc_classes[i].append(0)
                
            mask_te = (y_test == i)
            if np.sum(mask_te) > 0:
                test_acc_classes[i].append(accuracy_score(y_test[mask_te], y_test_pred[mask_te]))
            else:
                test_acc_classes[i].append(0)
                
    print("[+] Hoàn tất huấn luyện!")
    
    # Khởi tạo mô hình dự đoán chuẩn để người dùng nhập thông số dự đoán
    final_model = GaussianNB()
    final_model.fit(X_train, y_train)

    # 3. KHỐI MENU NHẬP XUẤT TƯƠNG TÁC
    while True:
        print("\n" + "="*70)
        print(" TÍNH NĂNG TƯƠNG TÁC: XEM BIỂU ĐỒ & DỰ ĐOÁN")
        print("="*70)
        print("1. Xem biểu đồ Epoch của riêng loài SETOSA")
        print("2. Xem biểu đồ Epoch của riêng loài VERSICOLOR")
        print("3. Xem biểu đồ Epoch của riêng loài VIRGINICA")
        print("4. Xem biểu đồ Epoch CHUNG (Của cả mô hình)")
        print("5. Nhập 4 kích thước để máy tính dự đoán loài hoa")
        print("6. Thoát chương trình")
        print("-" * 70)
        
        choice = input("=> Mời bạn chọn chức năng (1-6): ")
        
        if choice == '1':
            plot_epoch(train_acc_classes[0], test_acc_classes[0], "Biểu đồ Epoch - Loài SETOSA", "Epoch_Setosa.png", epochs)
        elif choice == '2':
            plot_epoch(train_acc_classes[1], test_acc_classes[1], "Biểu đồ Epoch - Loài VERSICOLOR", "Epoch_Versicolor.png", epochs)
        elif choice == '3':
            plot_epoch(train_acc_classes[2], test_acc_classes[2], "Biểu đồ Epoch - Loài VIRGINICA", "Epoch_Virginica.png", epochs)
        elif choice == '4':
            plot_epoch(train_acc, test_acc, "Biểu đồ Epoch - CHUNG (Toàn mô hình)", "Epoch_Chung.png", epochs)
        elif choice == '5':
            try:
                print("\n[+] DỰ ĐOÁN THỦ CÔNG")
                val1 = input("  - 1. Chiều dài đài hoa (Sepal length) tính bằng cm: ")
                val2 = input("  - 2. Chiều rộng đài hoa (Sepal width) tính bằng cm: ")
                val3 = input("  - 3. Chiều dài cánh hoa (Petal length) tính bằng cm: ")
                val4 = input("  - 4. Chiều rộng cánh hoa (Petal width) tính bằng cm: ")
                
                features = np.array([[float(val1), float(val2), float(val3), float(val4)]])
                pred_idx = final_model.predict(features)[0]
                pred_name = target_names[pred_idx]
                
                print(f"\n=> 🤖 KẾT QUẢ: Dựa trên số đo, mô hình đoán đây là giống hoa ** {pred_name.upper()} **")
            except ValueError:
                print("\n❌ Lỗi: Vui lòng nhập số hợp lệ (ví dụ: 5.1).")
        elif choice == '6':
            print("\nĐã thoát chương trình. Tạm biệt!")
            break
        else:
            print("\n❌ Lựa chọn không hợp lệ, vui lòng nhập số từ 1 đến 6.")

if __name__ == "__main__":
    main()