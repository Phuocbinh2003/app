import streamlit as st
import numpy as np
from PIL import Image

# Cấu hình ứng dụng Streamlit
st.set_page_config(layout="wide", page_title="Theo Dõi Vị Trí Chuột")

st.title("Tải Ảnh và Theo Dõi Vị Trí Chuột")

# Sidebar để tải ảnh
uploaded_file = st.sidebar.file_uploader("Tải ảnh lên", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    # Hiển thị kích thước ảnh
    width, height = image.size
    st.write(f"Kích thước ảnh: {width} x {height}")

    # Placeholder để hiển thị vị trí chuột
    mouse_pos_placeholder = st.empty()

    # JavaScript để theo dõi vị trí chuột
    st.markdown("""
        <script>
        const img = document.querySelector("img[alt='Ảnh đầu vào']");
        img.addEventListener('mousemove', function(event) {
            const rect = img.getBoundingClientRect();
            const x = event.clientX - rect.left; // Tọa độ X trong ảnh
            const y = event.clientY - rect.top; // Tọa độ Y trong ảnh
            
            // Gửi vị trí chuột về Streamlit
            window.parent.streamlit.setMousePosition({x: Math.round(x), y: Math.round(y)});
        });
        </script>
    """, unsafe_allow_html=True)

    # Hiển thị vị trí chuột
    if 'mouse_position' not in st.session_state:
        st.session_state.mouse_position = {'x': 0, 'y': 0}

    # Cập nhật vị trí chuột
    def update_mouse_position(data):
        st.session_state.mouse_position = data
        mouse_pos_placeholder.write(f"Vị trí chuột trong ảnh: (X: {st.session_state.mouse_position['x']}, Y: {st.session_state.mouse_position['y']})")

    # Cập nhật vị trí chuột khi có sự kiện
    update_mouse_position(st.session_state.mouse_position)

else:
    st.write("Vui lòng tải một bức ảnh lên.")
