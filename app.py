import streamlit as st
from PIL import Image
import requests

# Cấu hình ứng dụng Streamlit
st.set_page_config(layout="wide", page_title="Theo Dõi Vị Trí Chuột")

st.title("Tải Ảnh từ URL và Theo Dõi Vị Trí Chuột")

# URL của ảnh
image_url = "https://3jehonmevrh3tx299kue3g.streamlit.app:443/~/+/media/aeeb3fec9bff3b745a9c586a005cd646dad3575463f5454dd97bfc19.jpg"

# Tải ảnh từ URL
image = Image.open(requests.get(image_url, stream=True).raw)
st.image(image, caption='Ảnh đầu vào', use_column_width=True)

# Hiển thị kích thước ảnh
width, height = image.size
st.write(f"Kích thước ảnh: {width} x {height}")

# Placeholder để hiển thị vị trí chuột
mouse_pos_placeholder = st.empty()

# JavaScript để theo dõi vị trí chuột và ngăn chặn sự kiện nhấp chuột
st.markdown("""
    <script>
    const img = document.querySelector("img[alt='Ảnh đầu vào']");
    
    // Ngăn chặn sự kiện nhấp chuột
    img.addEventListener('mousedown', function(event) {
        event.preventDefault();
    });

    // Theo dõi vị trí chuột
    img.addEventListener('mousemove', function(event) {
        const rect = img.getBoundingClientRect();
        const x = Math.round(event.clientX - rect.left); // Tọa độ X trong ảnh
        const y = Math.round(event.clientY - rect.top); // Tọa độ Y trong ảnh
        
        // Gửi vị trí chuột về Streamlit
        window.parent.postMessage({x: x, y: y}, "*");
    });
    </script>
""", unsafe_allow_html=True)

# Cập nhật vị trí chuột từ tin nhắn
if 'mouse_position' not in st.session_state:
    st.session_state.mouse_position = {'x': 0, 'y': 0}

# Lắng nghe các tin nhắn từ JavaScript
def on_message(msg):
    if 'x' in msg and 'y' in msg:
        st.session_state.mouse_position = {'x': msg['x'], 'y': msg['y']}
        update_mouse_position()

# Cập nhật vị trí chuột
def update_mouse_position():
    mouse_pos_placeholder.write(f"Vị trí chuột trong ảnh: (X: {st.session_state.mouse_position['x']}, Y: {st.session_state.mouse_position['y']})")

# Đăng ký lắng nghe tin nhắn
st.session_state.on_message = on_message

# Gọi hàm cập nhật vị trí chuột
update_mouse_position()
