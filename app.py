import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import numpy as np

# Cấu hình ứng dụng Streamlit
st.set_page_config(layout="wide", page_title="Tải Ảnh Lên và Vẽ")

st.title("Tải Ảnh Lên và Vẽ Hình Chữ Nhật")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh để tải lên", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    
    # Convert image to numpy array (required for canvas background)
    image_np = np.array(image)

    # Hiển thị kích thước ảnh
    width, height = image.size
    st.write(f"Kích thước ảnh: {width} x {height}")

    # Thiết lập nét vẽ hình chữ nhật
    stroke_width = st.sidebar.slider("Độ rộng nét vẽ:", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Chọn màu vẽ:", "#FF0000")

    # Fill color with full transparency for rectangles
    fill_color = "rgba(0, 0, 0, 0.0)"  # Transparent fill

    # Display the image first
    st.image(image, caption="Ảnh đầu vào", use_column_width=True)

    # Add canvas as an overlay on top of the image
    canvas_result = st_canvas(
        fill_color=fill_color,               # Transparent fill
        stroke_width=stroke_width,           # Độ rộng nét vẽ
        stroke_color=stroke_color,           # Màu nét vẽ
        background_image=Image.fromarray(image_np),  # Ảnh nền là ảnh đã tải lên
        update_streamlit=True,
        drawing_mode="rect",                 # Chỉ cho phép vẽ hình chữ nhật
        height=height,
        width=width,
        key="canvas",
    )

    # Hiển thị kết quả canvas sau khi vẽ
    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data, caption="Ảnh sau khi vẽ", use_column_width=True)

else:
    st.write("Vui lòng tải lên một bức ảnh.")
