import streamlit as st
import numpy as np
from PIL import Image

# Cấu hình trang Streamlit
st.set_page_config(layout="wide", page_title="Fixed Background Image")

st.write("# Hình ảnh Nền Cố định")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    # Thêm một khung hình ẩn để xử lý sự kiện
    st.markdown(
        """
        <style>
        .fixed-image {
            position: relative;
            width: 100%;
            height: auto;
            pointer-events: none;  /* Ngăn chặn tương tác chuột */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Hiển thị ảnh
    st.image(image, caption='Ảnh cố định', use_column_width=True)

    # Thêm widget khác để xử lý các tương tác
    st.button("Nút Bất Kỳ", key="some_button")

    # Hiển thị thông tin hoặc điều khiển khác
    st.write("Thông tin khác hoặc các điều khiển khác ở đây.")
