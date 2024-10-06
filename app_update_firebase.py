import streamlit as st
import os
from Update_Firebase import add_student  # Import hàm add_student từ Update_Firebase.py

def run_app4():
    # Giao diện người dùng
    st.title("Tải Thông Tin Sinh Viên Lên")

    # Nhập thông tin sinh viên
    student_id = st.text_input("Mã Sinh Viên")
    Ten = st.text_input("Họ và Tên")
    Ngay_sinh = st.date_input("Ngày Sinh")
    Lop = st.text_input("Lớp")
    Khoa = st.text_input("Khoa")

    # Tải ảnh lên
    image_file_1 = st.file_uploader("Tải Ảnh Chân Dung", type=['jpg', 'jpeg', 'png'])
    image_file_2 = st.file_uploader("Tải Ảnh Thẻ Sinh Viên", type=['jpg', 'jpeg', 'png'])

    if st.button("Gửi Thông Tin"):
        if image_file_1 and image_file_2:
            # Lưu ảnh vào thư mục tạm thời
            image_file_1_path = f"temp_{student_id}_1.jpg"
            image_file_2_path = f"temp_{student_id}_2.jpg"

            with open(image_file_1_path, "wb") as f:
                f.write(image_file_1.getbuffer())

            with open(image_file_2_path, "wb") as f:
                f.write(image_file_2.getbuffer())

            # Thêm sinh viên và tải ảnh lên Firebase
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
