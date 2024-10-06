import firebase_admin
from firebase_admin import credentials, firestore, storage

# Khởi tạo ứng dụng Firebase bằng file key.json
cred = credentials.Certificate('phuocbinh2003-cf142-firebase-adminsdk-elr02-c3eb3c501c.json')
firebase_admin.initialize_app(cred)

# Khởi tạo Firestore và Storage
db = firestore.client()
bucket = storage.bucket()

# Hàm để upload ảnh lên Firebase Storage
def upload_image(student_id, image_path, image_type):
    blob = bucket.blob(f'student-images/{student_id}/{image_type}.jpg')
    blob.upload_from_filename(image_path)
    print(f"Image {image_type} uploaded successfully.")

# Thêm thông tin sinh viên vào Firestore
def add_student(student_id, Ten, Ngay_sinh, Lop, Khoa, image_file_1, image_file_2):
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
