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

    # Hiển thị vị trí chuột
    mouse_position = st.empty()  # Tạo không gian hiển thị vị trí chuột

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

    # JavaScript để theo dõi vị trí chuột
    st.markdown(
        """
        <script>
        const img = document.querySelector('img');
        img.addEventListener('mousemove', function(event) {
            const rect = img.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            const mousePosition = `(${Math.round(x)}, ${Math.round(y)})`;
            window.parent.postMessage({ type: 'mouse_position', position: mousePosition }, '*');
        });
        </script>
        """,
        unsafe_allow_html=True
    )

    # Xử lý thông điệp từ JavaScript
    if 'position' in st.session_state:
        pos = st.session_state.position
        mouse_position.text(f"Vị trí chuột: {pos}")
    else:
        mouse_position.text("Vị trí chuột: (0, 0)")

# Lắng nghe các thông điệp từ JavaScript
st.session_state.mouse_position = st.empty()  # Tạo không gian hiển thị cho vị trí chuột
if st.button('Cập nhật vị trí chuột'):
    pos = st.session_state.position if 'position' in st.session_state else "(0, 0)"
    st.session_state.mouse_position.text(f"Vị trí chuột: {pos}")
