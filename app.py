import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import numpy as np

# Cấu hình ứng dụng Streamlit
st.set_page_config(layout="wide", page_title="Tải Ảnh và Vẽ Trên Ảnh")

st.title("Tải Ảnh Lên và Vẽ Trên Ảnh")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh để tải lên", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    
    # Convert the image to RGBA format to ensure it's compatible
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    # Chuyển đổi ảnh thành mảng numpy để sử dụng trong canvas
    image_np = np.array(image)

    # Hiển thị kích thước ảnh
    width, height = image.size
    st.write(f"Kích thước ảnh: {width} x {height}")

    # Thiết lập canvas để vẽ lên ảnh
    drawing_mode = st.sidebar.selectbox("Chọn chế độ vẽ:", ("Vẽ tự do", "Vẽ hình chữ nhật"))
    stroke_width = st.sidebar.slider("Độ rộng nét vẽ:", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Chọn màu vẽ:", "#000000")

    # Transparency setting for drawing (set alpha value for transparency)
    fill_color = "rgba(255, 165, 0, 0.0)"  # Fully transparent (alpha = 0.0)

    # Canvas setup
    canvas_result = st_canvas(
        fill_color=fill_color,               # Màu tô trong suốt
        stroke_width=stroke_width,           # Độ rộng nét vẽ
        stroke_color=stroke_color,           # Màu vẽ
        background_image=image_np,           # Ảnh nền để vẽ lên
        update_streamlit=True,
        drawing_mode="freedraw" if drawing_mode == "Vẽ tự do" else "rect",
        height=height,
        width=width,
        key="canvas",
    )

    # Hiển thị kết quả canvas sau khi vẽ
    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data, caption="Ảnh sau khi vẽ", use_column_width=True)

else:
    st.write("Vui lòng tải lên một bức ảnh.")
