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

    # Hiển thị ảnh
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    # JavaScript để theo dõi sự kiện chuột di chuyển vào và ra khỏi ảnh
    st.markdown("""
        <script>
        const img = document.querySelector('img');
        img.addEventListener('mouseenter', function() {
            document.dispatchEvent(new CustomEvent('mouseInImage', {detail: true}));
        });

        img.addEventListener('mouseleave', function() {
            document.dispatchEvent(new CustomEvent('mouseInImage', {detail: false}));
        });
        </script>
    """, unsafe_allow_html=True)

    # Theo dõi sự kiện từ JavaScript
    st.markdown("""
        <script>
        document.addEventListener('mouseInImage', function(e) {
            const input = window.parent.document.querySelector('input[data-testid="mouse_in_image"]');
            input.value = e.detail;
            input.dispatchEvent(new Event('input', {bubbles: true}));
        });
        </script>
    """, unsafe_allow_html=True)

    # Khởi tạo trạng thái nếu chưa có
    if "mouse_in_image" not in st.session_state:
        st.session_state["mouse_in_image"] = False

    # Hiển thị trạng thái chuột có trong ảnh hay không
    mouse_in_image = st.text_input("Mouse in Image:", value=str(st.session_state["mouse_in_image"]), key="mouse_in_image")

    if mouse_in_image == "True":
        st.write("Đã vào bức ảnh")
    else:
        st.write("Chưa vào bức ảnh")
