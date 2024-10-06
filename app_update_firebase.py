import streamlit as st
import os
import requests
from firebase_admin import firestore, storage, credentials
import firebase_admin

# Tải tệp JSON từ GitHub
def download_json_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open('firebase_credentials.json', 'wb') as f:
            f.write(response.content)
        return 'firebase_credentials.json'
    else:
        raise Exception("Không thể tải tệp JSON.")

# Đường dẫn tới tệp JSON trong kho GitHub của bạn
json_url = 'https://raw.githubusercontent.com/Phuocbinh2003/app/063fc630eba23414d94b5e8f989519ae51c7c034/phuocbinh2003-cf142-firebase-adminsdk-elr02-c3eb3c501c.json'

# Tải tệp JSON
cred_path = download_json_from_github(json_url)
cred = credentials.Certificate(cred_path)

# Khởi tạo Firebase app
firebase_admin.initialize_app(cred, {'storageBucket': 'phuocbinh2003-cf142.appspot.com'})

# Khởi tạo Firestore và Storage
db = firestore.client()
bucket = storage.bucket()

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

            # Xóa các file tạm sau khi upload
            os.remove(image_file_1_path)
            os.remove(image_file_2_path)
        else:
            st.error("Vui lòng tải lên cả hai ảnh.")

if __name__ == "__main__":
    run_app4()
