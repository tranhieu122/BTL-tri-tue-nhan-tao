import sys
import os

# Thêm thư mục backend vào sys.path để import các module
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'backend'))
sys.path.insert(0, backend_dir)

# Import app Flask từ src/backend/app.py
from app import app

if __name__ == '__main__':
    # Chạy server ở port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)
