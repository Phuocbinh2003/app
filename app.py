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
    mouse_in_image = st.empty()  # Tạo không gian hiển thị trạng thái chuột

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

    # Lắng nghe sự kiện chuột
    mouse_x = st.text_input("Mouse X:", "")
    mouse_y = st.text_input("Mouse Y:", "")
    
    # Cập nhật vị trí chuột
    if mouse_x and mouse_y:
        mouse_position.text(f"Vị trí chuột: ({mouse_x}, {mouse_y})")
        mouse_in_image.text("Đã vào bức ảnh")
    else:
        mouse_position.text("Vị trí chuột: (0, 0)")
        mouse_in_image.text("Chưa vào bức ảnh")
