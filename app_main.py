import streamlit as st
from GrabCut_app import run_app1

from app_face_detection import run_app3
from app_update_firebase import run_app4

# Tạo thanh điều hướng
option = st.sidebar.selectbox(
    'Chọn ứng dụng:',
    ('GrabCut','app2','Face_Verification','Update_firebase')  # Đã loại bỏ Ứng dụng 2 nếu không sử dụng
)

# Hiển thị ứng dụng tương ứng
if option == 'GrabCut':
    run_app1()  # Gọi hàm chạy ứng dụng 1

elif option == 'Face_Verification':
    run_app3()  # Gọi hàm chạy ứng dụng 3
elif option == 'Update_firebase':
    run_app4()  # Gọi hàm chạy ứng dụng 4
else:
    st.write("Vui lòng chọn một ứng dụng từ thanh điều hướng.")
