import streamlit as st
import numpy as np
from PIL import Image
import cv2
from grabcut_processor import GrabCutProcessor
import io

# Cấu hình trang Streamlit
st.set_page_config(layout="wide", page_title="Deploy GrabCut")

st.write("# Xóa Background GrabCut")

st.divider()

st.markdown("""
    ## Hướng dẫn cách dùng
    
    * Chọn chế độ vẽ bằng các phím sau:
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

    # Tùy chọn để chọn chế độ vẽ
    st.sidebar.write("## Chọn chế độ vẽ")
    draw_mode = st.sidebar.radio("Chọn chế độ:", ('Sure BG (0)', 'Sure FG (1)', 'Prob BG (2)', 'Prob FG (3)'))

    # Map chế độ vẽ thành giá trị trong GrabCutProcessor
    if draw_mode == 'Sure BG (0)':
        grabcut_processor.value = grabcut_processor.DRAW_BG
    elif draw_mode == 'Sure FG (1)':
        grabcut_processor.value = grabcut_processor.DRAW_FG
    elif draw_mode == 'Prob BG (2)':
        grabcut_processor.value = grabcut_processor.DRAW_PR_BG
    elif draw_mode == 'Prob FG (3)':
        grabcut_processor.value = grabcut_processor.DRAW_PR_FG

    # Nút cập nhật và reset
    if st.sidebar.button("Cập nhật phân đoạn (n)"):
        grabcut_processor.apply_grabcut()

    if st.sidebar.button("Thiết lập lại (r)"):
        grabcut_processor.reset()

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
