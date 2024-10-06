import streamlit as st
import os
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Kiểm tra xem ứng dụng đã được khởi tạo chưa
if not firebase_admin._apps:
    cred = credentials.Certificate('phuocbinh2003-cf142-firebase-adminsdk-elr02-f9b51abc60.json')
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'phuocbinh2003-cf142.appspot.com'
    })

app = firebase_admin.get_app()
db = firestore.client(app)  # Kết nối với Firestore
bucket = storage.bucket()  # Kết nối với Firebase Storage

def upload_image(student_id, image_path, image_type):
    blob = bucket.blob(f'student-images/{student_id}/{image_type}.jpg')
    blob.upload_from_filename(image_path)
    st.success(f"Image {image_type} uploaded successfully.")

def add_student(student_id, Ten, Ngay_sinh, Lop, Khoa, image_file_1, image_file_2):
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

def run_app4():
    st.title("Tải Thông Tin Sinh Viên Lên")

    student_id = st.text_input("Mã Sinh Viên")
    Ten = st.text_input("Họ và Tên")
    Ngay_sinh = st.date_input("Ngày Sinh")
    Lop = st.text_input("Lớp")
    Khoa = st.text_input("Khoa")

    image_file_1 = st.file_uploader("Tải Ảnh Chân Dung", type=['jpg', 'jpeg', 'png'])
    image_file_2 = st.file_uploader("Tải Ảnh Thẻ Sinh Viên", type=['jpg', 'jpeg', 'png'])

    if st.button("Gửi Thông Tin"):
        if image_file_1 is not None and image_file_2 is not None:
            image_file_1_path = f"temp_{student_id}_1.jpg"
            image_file_2_path = f"temp_{student_id}_2.jpg"

            with open(image_file_1_path, "wb") as f:
                f.write(image_file_1.getbuffer())

            with open(image_file_2_path, "wb") as f:
                f.write(image_file_2.getbuffer())

            try:
                message = add_student(student_id, Ten, Ngay_sinh, Lop, Khoa, image_file_1_path, image_file_2_path)
                st.success(message)
            except Exception as e:
                st.error(f"Đã xảy ra lỗi: {str(e)}")

            os.remove(image_file_1_path)
            os.remove(image_file_2_path)
        else:
            st.error("Vui lòng tải lên cả hai ảnh.")

if __name__ == "__main__":
    run_app4()
