import streamlit as st
from GrabCut_app import run_app1
from app_face_detection import run_app3

# Lấy các tham số truy vấn từ URL
query_params = st.experimental_get_query_params()

# Kiểm tra xem có tham số 'app' không và lấy giá trị của nó
selected_app = query_params.get("app", [None])[0]

# Tạo thanh điều hướng
if selected_app is None:
    option = st.sidebar.selectbox(
        'Chọn ứng dụng:',
        ('Ứng dụng 1', 'Ứng dụng 3')  # Đã loại bỏ Ứng dụng 2 nếu không sử dụng
    )
else:
    option = selected_app

# Hiển thị ứng dụng tương ứng
if option == 'Ứng dụng 1':
    run_app1()  # Gọi hàm chạy ứng dụng 1
elif option == 'Ứng dụng 3':
    run_app3()  # Gọi hàm chạy ứng dụng 3
else:
    st.write("Vui lòng chọn một ứng dụng từ thanh điều hướng.")
