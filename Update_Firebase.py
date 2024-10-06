import os
import firebase_admin
from firebase_admin import credentials, firestore, storage
from dotenv import load_dotenv
import json

# Tải biến môi trường từ file .env
load_dotenv()

# Lấy thông tin xác thực từ biến môi trường
firebase_key = os.getenv('FIREBASE_KEY')

# Kiểm tra xem ứng dụng Firebase đã được khởi tạo chưa
if not firebase_admin._apps:
    # Chuyển đổi chuỗi JSON thành đối tượng JSON
    cred = credentials.Certificate(json.loads(firebase_key))
    
    # Khởi tạo ứng dụng Firebase với tên bucket
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'phuocbinh2003-cf142.appspot.com'  # Thay đổi tên bucket ở đây
    })

# Khởi tạo Firestore và Storage
db = firestore.client()
bucket = storage.bucket()

# Hàm để upload ảnh lên Firebase Storage
def upload_image(student_id, image_path, image_type):
    try:
        blob = bucket.blob(f'student-images/{student_id}/{image_type}.jpg')
        blob.upload_from_filename(image_path)
        print(f"Image {image_type} uploaded successfully.")
    except Exception as e:
        print(f"Failed to upload image {image_type}: {e}")

# Thêm thông tin sinh viên vào Firestore
def add_student(student_id, Ten, Ngay_sinh, Lop, Khoa, image_file_1, image_file_2):
    try:
        # Thêm dữ liệu sinh viên vào Firestore
        doc_ref = db.collection('students').document(student_id)
        doc_ref.set({
            'Ten': Ten,
            'Ngay_sinh': Ngay_sinh,
            'Lop': Lop,
            'Khoa': Khoa
        })

        # Tải ảnh lên Firebase Storage
        upload_image(student_id, image_file_1, 'photo_Chan_dung')
        upload_image(student_id, image_file_2, 'photo_The_sinh_vien')

        return f"Data for student {Ten} has been uploaded successfully."
    except Exception as e:
        return f"Failed to add student {Ten}: {e}"
