import streamlit as st

def run_app4():
    # Giao diện người dùng
    st.title("Upload Student Information")
    
    # Nhập thông tin sinh viên
    student_id = st.text_input("Student ID")
    Ten = st.text_input("Name")
    Ngay_sinh = st.date_input("Date of Birth")
    Lop = st.text_input("Class")
    Khoa = st.text_input("Department")
    
    # Tải ảnh lên
    image_file_1 = st.file_uploader("Upload Portrait Photo", type=['jpg', 'jpeg', 'png'])
    image_file_2 = st.file_uploader("Upload Student ID Photo", type=['jpg', 'jpeg', 'png'])
    
    if st.button("Submit"):
        if image_file_1 and image_file_2:
            # Lưu ảnh vào thư mục tạm thời
            image_file_1_path = f"temp_{student_id}_1.jpg"
            image_file_2_path = f"temp_{student_id}_2.jpg"
            
            with open(image_file_1_path, "wb") as f:
                f.write(image_file_1.getbuffer())
            
            with open(image_file_2_path, "wb") as f:
                f.write(image_file_2.getbuffer())
            
            # Thêm sinh viên và tải ảnh
            message = add_student(student_id, Ten, Ngay_sinh, Lop, Khoa, image_file_1_path, image_file_2_path)
            st.success(message)
    
            # Xóa các file tạm sau khi upload
            os.remove(image_file_1_path)
            os.remove(image_file_2_path)
        else:
            st.error("Please upload both images.")
            
