import streamlit as st
from GrabCut_app import run_app1
from app_face_detection import run_app3

# Tạo thanh điều hướng
option = st.sidebar.selectbox(
    'Chọn ứng dụng:',
    ('Ứng dụng 1', 'Ứng dụng 3','Ứng dụng 4')  # Đã loại bỏ Ứng dụng 2 nếu không sử dụng
)

# Hiển thị ứng dụng tương ứng
if option == 'Ứng dụng 1':
    run_app1()  # Gọi hàm chạy ứng dụng 1
elif option == 'Ứng dụng 3':
    run_app3()  # Gọi hàm chạy ứng dụng 3
elif option == 'Ứng dụng 4':
    run_app4()  # Gọi hàm chạy ứng dụng 4
else:
    st.write("Vui lòng chọn một ứng dụng từ thanh điều hướng.")
