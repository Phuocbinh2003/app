import streamlit as st
import numpy as np
from PIL import Image
import io
import cv2
from grabcut_processor import GrabCutProcessor

# Cấu hình trang Streamlit
st.set_page_config(layout="wide", page_title="Deploy GrabCut")

st.write("# Xóa Background GrabCut")

st.divider()

st.markdown("""
    ## Hướng dẫn cách dùng

    * Vẽ hình chữ nhật trước (vẽ bằng click phải)
    * Sử dụng phím (chọn phím sau đó vẽ bằng click trái):
        * Phím '0' - Để chọn các vùng có sure background
        * Phím '1' - Để chọn các vùng có sure foreground
        * Phím '2' - Để chọn các vùng probable background
        * Phím '3' - Để chọn các vùng probable foreground
        * Phím 'n' - Để cập nhật phân đoạn
        * Phím 'r' - Để thiết lập lại 
""")

st.divider()

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    image = np.array(image)

    # Khởi tạo GrabCutProcessor
    grabcut_processor = GrabCutProcessor(image)

    # Phần xử lý ảnh
    st.write("### Kết quả")
    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        st.image(image, caption='Ảnh đầu vào', use_column_width=True)

    with col2:
        st.image(grabcut_processor.get_output_image(), caption='Ảnh được phân đoạn', use_column_width=True)

    # Nút tải ảnh
    output_image_pil = Image.fromarray(cv2.cvtColor(grabcut_processor.get_output_image(), cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    output_image_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Tải ảnh xuống",
        data=byte_im,
        file_name="segmented_image.png",
        mime="image/png"
    )

    # HTML and JavaScript for mouse position tracking
    st.markdown("""
        <script>
        const img = document.querySelector('img[alt="Ảnh đầu vào"]');
        img.addEventListener('mousemove', function(event) {
            const rect = img.getBoundingClientRect();
            const x = Math.round(event.clientX - rect.left);
            const y = Math.round(event.clientY - rect.top);
            const mousePos = {x: x, y: y};
            window.parent.postMessage(mousePos, "*");
        });
        </script>
    """, unsafe_allow_html=True)

    # Listen for messages from the JavaScript
    if "mouse_position" in st.session_state:
        mouse_x, mouse_y = st.session_state.mouse_position
    else:
        mouse_x, mouse_y = 0, 0

    # Display mouse position
    st.write(f"Vị trí chuột: ({mouse_x}, {mouse_y})")
