import streamlit as st
import numpy as np
from PIL import Image
import cv2
import io

# Hàm để xử lý ảnh vẽ lên
def draw_circle(image, x, y, color=(255, 0, 0), thickness=5):
    # Vẽ vòng tròn lên ảnh
    cv2.circle(image, (x, y), thickness, color, -1)
    return image

# Cấu hình trang Streamlit
st.set_page_config(layout="wide", page_title="Deploy GrabCut")

st.write("# Xóa Background GrabCut")

# CSS để thay đổi con trỏ khi di chuột vào hình ảnh
st.markdown("""
    <style>
    .crosshair-cursor {
        cursor: crosshair;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    image = np.array(image)

    # Lưu ảnh đã vẽ vào bộ nhớ tạm
    img_drawn = image.copy()

    # Hiển thị ảnh ban đầu
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    # Tích hợp JavaScript để xử lý sự kiện chuột
    st.markdown("""
        <script>
        const img = document.querySelector('img');
        let isDrawing = false;

        img.addEventListener('mousedown', function(e) {
            isDrawing = true;
        });

        img.addEventListener('mousemove', function(e) {
            if (isDrawing) {
                const rect = e.target.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                document.querySelector('input[name="mouse_x"]').value = x;
                document.querySelector('input[name="mouse_y"]').value = y;
                document.querySelector('input[name="is_drawing"]').value = true;
            }
        });

        img.addEventListener('mouseup', function() {
            isDrawing = false;
        });
        </script>
    """, unsafe_allow_html=True)

    # Các input ẩn để lưu trạng thái và tọa độ chuột
    mouse_x = st.text_input("X:", key="mouse_x", value="0")
    mouse_y = st.text_input("Y:", key="mouse_y", value="0")
    is_drawing = st.text_input("Drawing:", key="is_drawing", value="False")

    # Chuyển đổi tọa độ chuột thành số nguyên
    mouse_x = int(mouse_x)
    mouse_y = int(mouse_y)
    is_drawing = is_drawing == "True"

    # Nếu đang vẽ, thì vẽ lên ảnh
    if is_drawing:
        img_drawn = draw_circle(img_drawn, mouse_x, mouse_y)

    # Hiển thị ảnh đã vẽ
    st.image(img_drawn, caption='Ảnh đã vẽ', use_column_width=True)

    # Nút tải ảnh xuống
    output_image_pil = Image.fromarray(cv2.cvtColor(img_drawn, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    output_image_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Tải ảnh xuống",
        data=byte_im,
        file_name="drawn_image.png",
        mime="image/png"
    )
