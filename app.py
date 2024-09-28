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
    
    * Nhấn chuột trái để vẽ hình chữ nhật.
    * Nhấn nút 'Cập nhật' để áp dụng GrabCut.
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

    # Hiển thị ảnh và khung hình
    st.image(grabcut_processor.img, caption='Ảnh đầu vào', use_column_width=True)

    # Nút Cập nhật
    if st.button("Cập nhật"):
        grabcut_processor.apply_grabcut()
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
