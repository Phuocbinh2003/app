import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Cấu hình ứng dụng Streamlit
st.set_page_config(layout="wide", page_title="Tải Ảnh và Vẽ Hình Chữ Nhật")

st.title("Tải Ảnh Lên và Vẽ Hình Chữ Nhật")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Chọn ảnh để tải lên", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    
    # Hiển thị kích thước ảnh
    width, height = image.size
    st.write(f"Kích thước ảnh: {width} x {height}")

    # Canvas setup - chỉ cho phép vẽ hình chữ nhật
    stroke_width = st.sidebar.slider("Độ rộng nét vẽ:", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Chọn màu vẽ:", "#000000")

    # Transparency setting for fill (make it transparent)
    fill_color = "rgba(255, 165, 0, 0.0)"  # Fully transparent

    # Vẽ canvas với ảnh nền và chế độ vẽ hình chữ nhật
    canvas_result = st_canvas(
        fill_color=fill_color,               # Màu tô trong suốt
        stroke_width=stroke_width,           # Độ rộng nét vẽ
        stroke_color=stroke_color,           # Màu vẽ
        background_image=image,              # Ảnh nền
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
