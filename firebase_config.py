# firebase_config.py
import firebase_admin
from firebase_admin import credentials

# Kiểm tra xem ứng dụng đã được khởi tạo chưa
if not firebase_admin._apps:
    cred = credentials.Certificate('phuocbinh2003-cf142-firebase-adminsdk-elr02-c3eb3c501c.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'phuocbinh2003-cf142.appspot.com'  # Đảm bảo tên bucket là chính xác
    })
