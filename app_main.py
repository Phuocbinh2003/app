import streamlit as st
from GrabCut_app import run_app1
from app2 import run_app2
from app3 import run_app3

# Tạo tiêu đề cho ứng dụng chính
st.title("Ứng dụng tổng hợp")

# Tạo thanh điều hướng
option = st.sidebar.selectbox(
    'Chọn ứng dụng:',
    ('Ứng dụng 1', 'Ứng dụng 2', 'Ứng dụng 3')
)

# Hiển thị ứng dụng tương ứng
if option == 'Ứng dụng 1':
    run_app1()  # Gọi hàm chạy ứng dụng 1
elif option == 'Ứng dụng 2':
    run_app2()  # Gọi hàm chạy ứng dụng 2
elif option == 'Ứng dụng 3':
    run_app3()  # Gọi hàm chạy ứng dụng 3
