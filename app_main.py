import streamlit as st
from GrabCut_app import run_app1
from Watershed_Segmentation import run_app2  # Đã sửa tên module không có khoảng trắng
from app_face_detection import run_app3
from app_update_firebase import run_app4
from App_Face_Verification import run_app5

# Tạo thanh điều hướn
option = st.sidebar.selectbox(
    'Chọn ứng dụng:',
    ('GrabCut', 'App2','Face_detection','Update_firebase','Face_Verification')  # Đã loại bỏ Ứng dụng 2 nếu không sử dụng
)

# Hiển thị ứng dụng tương ứng
if option == 'GrabCut':
    run_app1()  # Gọi hàm chạy ứng dụng 1
elif option == 'App2':
    run_app2()  # Gọi hàm chạy ứng dụng 2
elif option == 'Face_detection':
    run_app3()  # Gọi hàm chạy ứng dụng 3
elif option == 'Update_firebase':
    run_app4()  # Gọi hàm chạy ứng dụng 4
elif option == 'Face_Verification':
    run_app5()  # Gọi hàm chạy ứng dụng 5
else:
    st.write("Vui lòng chọn một ứng dụng từ thanh điều hướng.")
