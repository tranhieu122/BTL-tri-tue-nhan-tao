import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=42, stratify=y)

nb = GaussianNB()
classes = np.unique(y)

train_acc = []
test_acc = []

# Để tạo ra độ nhiễu (wobbly) giống biểu đồ gốc, ta sẽ reset model sau mỗi vài epoch,
# hoặc ta tăng dần dữ liệu theo từng epoch.
# Dưới đây là cách mô phỏng học tăng cường (Online Learning) với batch nhỏ
epochs = 45
np.random.seed(42)

for epoch in range(1, epochs + 1):
    # Lấy một batch ngẫu nhiên
    idx = np.random.choice(len(X_train), size=max(5, epoch*2), replace=False)
    X_batch = X_train[idx]
    y_batch = y_train[idx]
    
    # partial_fit giúp mô hình học thêm từ từ
    nb.partial_fit(X_batch, y_batch, classes=classes)
    
    # Dự đoán và tính độ chính xác
    y_train_pred = nb.predict(X_train)
    y_test_pred = nb.predict(X_test)
    
    train_acc.append(accuracy_score(y_train, y_train_pred))
    test_acc.append(accuracy_score(y_test, y_test_pred))

# Vẽ biểu đồ y hệt hình mẫu
plt.figure(figsize=(8, 5))
plt.plot(train_acc, label='Train', linewidth=2.5, color='#1f77b4') # Màu xanh
plt.plot(test_acc, label='Test', linewidth=2.5, color='#d62728')  # Màu đỏ
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc='upper left')
plt.grid(True, linestyle='-', alpha=0.5, color='gray')
plt.savefig('test_plot.png')
print("Done!")
