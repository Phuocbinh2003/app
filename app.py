import streamlit as st
import cv2
import numpy as np
from PIL import Image

# Cấu hình trang Streamlit
st.set_page_config(layout="wide", page_title="Mouse Position Tracking with OpenCV")

st.write("# Theo dõi vị trí chuột trên hình ảnh với OpenCV")

# Sidebar để tải ảnh
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])

# Khởi tạo session_state nếu chưa có
if 'mouse_x' not in st.session_state:
    st.session_state.mouse_x = None
if 'mouse_y' not in st.session_state:
    st.session_state.mouse_y = None

# Hàm để theo dõi sự kiện chuột với OpenCV
def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        st.session_state.mouse_x = x
        st.session_state.mouse_y = y

if uploaded_file is not None:
    # Đọc ảnh
    image = Image.open(uploaded_file)
    image = np.array(image)

    # Tạo cửa sổ OpenCV
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", on_mouse)

    # Hiển thị ảnh trong OpenCV
    while True:
        img_copy = image.copy()

        # Hiển thị vị trí chuột nếu có
        if st.session_state.mouse_x is not None and st.session_state.mouse_y is not None:
            cv2.putText(img_copy, f"X: {st.session_state.mouse_x}, Y: {st.session_state.mouse_y}", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Image", img_copy)

        # Nhấn phím 'q' để thoát
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    # Hiển thị ảnh đã chỉnh sửa trên Streamlit
    st.image(image, caption='Ảnh đầu vào', use_column_width=True)
