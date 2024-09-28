import streamlit as st
import numpy as np
from PIL import Image
import cv2

# Cấu hình trang Streamlit
st.set_page_config(layout="wide", page_title="Mouse Position Tracking")

st.write("# Theo dõi vị trí chuột trên hình ảnh")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    image = np.array(image)

    # Hiển thị ảnh trong Streamlit
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    # Tạo một thẻ HTML để theo dõi vị trí chuột
    st.markdown(
        """
        <style>
        .mouse-info {
            position: relative;
            color: white;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 5px;
            border-radius: 5px;
            display: inline-block;
        }
        </style>
        <div id="mouse-position" class="mouse-info"></div>
        <script>
        const img = document.querySelector("img");
        img.addEventListener("mousemove", (event) => {
            const rect = img.getBoundingClientRect();
            const x = Math.round(event.clientX - rect.left);
            const y = Math.round(event.clientY - rect.top);
            const mouseInfo = document.getElementById("mouse-position");
            mouseInfo.style.left = event.clientX + "px";
            mouseInfo.style.top = event.clientY + "px";
            mouseInfo.innerHTML = "X: " + x + ", Y: " + y;
        });
        </script>
        """,
        unsafe_allow_html=True
    )
