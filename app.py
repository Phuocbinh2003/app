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

def remove_even_pixels(image):
    # Chuyển đổi ảnh sang định dạng NumPy array
    img_array = np.array(image)
    
    # Tạo một mask cho các pixel có vị trí chẵn
    mask = (np.indices(img_array.shape[:2]) % 2 == 0).all(axis=0)

    # Đặt các pixel chẵn thành màu trắng (hoặc giá trị khác nếu cần)
    img_array[mask] = [255, 255, 255]  # Màu trắng

    return img_array

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    image = np.array(image)

    # Khởi tạo GrabCutProcessor
    grabcut_processor = GrabCutProcessor(image)

    # Xóa các pixel chẵn trong ảnh
    modified_image = remove_even_pixels(image)

    # Phần xử lý ảnh
    st.write("### Kết quả")
    col1, col2 = st.columns([0.5, 0.5])

    with col1:
        # Disable pointer events on the original image
        st.markdown(f'<div style="pointer-events: none;">{st.image(image, caption="Ảnh đầu vào", use_column_width=True)}</div>', unsafe_allow_html=True)

    with col2:
        # Disable pointer events on the modified image
        st.markdown(f'<div style="pointer-events: none;">{st.image(modified_image, caption="Ảnh sau khi xóa pixel chẵn", use_column_width=True)}</div>', unsafe_allow_html=True)

    # Nút tải ảnh
    output_image_pil = Image.fromarray(cv2.cvtColor(modified_image, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO()
    output_image_pil.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Tải ảnh xuống",
        data=byte_im,
        file_name="modified_image.png",
        mime="image/png"
    )

    # Hiển thị vị trí chuột (không cần thiết, có thể xóa nếu không cần)
    st.write("Vị trí chuột: (0, 0)")  # Chỉ để giữ lại giao diện, có thể xóa
