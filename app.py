import streamlit as st
import numpy as np
from PIL import Image

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

    # Hiển thị ảnh với lớp CSS cho con trỏ
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    # JavaScript để theo dõi sự kiện chuột di chuyển vào và ra khỏi ảnh
    st.markdown("""
        <script>
        const img = document.querySelector('img');
        img.addEventListener('mouseenter', function() {
            document.querySelector('input[name="mouse_in_image"]').value = 'True';
            document.querySelector('input[name="submit-button"]').click();
        });

        img.addEventListener('mouseleave', function() {
            document.querySelector('input[name="mouse_in_image"]').value = 'False';
            document.querySelector('input[name="submit-button"]').click();
        });
        </script>
    """, unsafe_allow_html=True)

    # Input ẩn để lưu trạng thái chuột có vào ảnh hay không
    mouse_in_image = st.text_input("Mouse in Image:", key="mouse_in_image", value="False")
    
    # Nút submit ẩn để cập nhật trạng thái mỗi khi có sự thay đổi từ JavaScript
    st.text_input("Submit Button:", key="submit-button", type="hidden")

    # Kiểm tra xem chuột đã vào ảnh hay chưa
    if mouse_in_image == "True":
        st.write("Đã vào bức ảnh")
    else:
        st.write("Chưa vào bức ảnh")

