import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import numpy as np

# Cấu hình ứng dụng Streamlit
st.set_page_config(layout="wide", page_title="Vẽ Trên Ảnh")

st.title("Tải Ảnh Lên và Vẽ Hình Chữ Nhật Trực Tiếp Trên Ảnh")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh để tải lên", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh và chuyển thành numpy array để sử dụng làm nền cho canvas
    image = Image.open(uploaded_file)
    image_np = np.array(image)  # Convert to NumPy array for canvas background

    # Lấy kích thước ảnh gốc
    original_width, original_height = image.size

    # Xác định kích thước canvas theo tỷ lệ màn hình
    max_canvas_width = st.sidebar.slider("Chọn kích thước canvas tối đa (px):", 300, 1200, 700)
    ratio = max_canvas_width / original_width
    new_height = int(original_height * ratio)
    
    # Hiển thị ảnh đầu vào
    st.image(image, caption="Ảnh đầu vào", use_column_width=False, width=max_canvas_width)

    # Sidebar: Thiết lập cho nét vẽ hình chữ nhật
    stroke_width = st.sidebar.slider("Độ rộng nét vẽ:", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Chọn màu vẽ:", "#FF0000")

    # Tạo canvas với kích thước dựa trên ảnh
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",        # Transparent fill
        stroke_width=stroke_width,            # Độ rộng nét vẽ
        stroke_color=stroke_color,            # Màu vẽ
        background_image=Image.fromarray(image_np),  # Đặt ảnh nền là ảnh đã tải lên
        update_streamlit=True,
        drawing_mode="rect",                  # Chỉ cho phép vẽ hình chữ nhật
        height=new_height,                    # Set chiều cao của canvas
        width=max_canvas_width,               # Set chiều rộng của canvas
        key="canvas",
    )

    # Hiển thị kết quả canvas sau khi vẽ
    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data, caption="Ảnh sau khi vẽ", use_column_width=False, width=max_canvas_width)

else:
    st.write("Vui lòng tải lên một bức ảnh.")
