import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image

# Hàm để áp dụng Watershed
def apply_watershed(img, kernel_size, distance_thresh_factor, dilation_iterations):
    # Resize ảnh
    img = cv.resize(img, (500, 400))

    # Chuyển sang ảnh xám và nhị phân Otsu
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Áp dụng dilation
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated = cv.dilate(binary, kernel, iterations=dilation_iterations)

    # Distance transform và ngưỡng hóa
    dist_transform = cv.distanceTransform(dilated, cv.DIST_L2, 5)
    _, sure_fg = cv.threshold(dist_transform, distance_thresh_factor * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Marker cho Watershed
    _, markers = cv.connectedComponents(sure_fg)
    markers = markers + 1
    markers[cv.subtract(cv.dilate(sure_fg, kernel, iterations=3), sure_fg) == 255] = 0

    # Áp dụng Watershed
    img_markers = img.copy()
    cv.watershed(img_markers, markers)
    img_markers[markers == -1] = [0, 0, 255]  # Viền màu đỏ

    return img_markers

# Ứng dụng Streamlit
def run_app2():
    st.title("Phân đoạn ký tự bằng Watershed")

    # Tải ảnh lên
    uploaded_image = st.file_uploader("Tải ảnh biển số lên", type=["jpg", "png", "jpeg"])

    # Sidebar cho tham số Watershed
    st.sidebar.header("Tham số Watershed")
    kernel_size = st.sidebar.slider("Kích thước kernel", min_value=1, max_value=15, value=3, step=1, key="kernel_size")
    distance_thresh_factor = st.sidebar.slider("Ngưỡng Distance Transform", min_value=0.1, max_value=1.0, value=0.3, step=0.1, key="distance_thresh_factor")
    dilation_iterations = st.sidebar.slider("Số lần Dilation", min_value=1, max_value=10, value=3, step=1, key="dilation_iterations")

    # Trạng thái lưu kết quả
    if "processed_result" not in st.session_state:
        st.session_state.processed_result = None

    # Kiểm tra nếu slider hoặc ảnh thay đổi
    if uploaded_image is not None:
        img = np.array(Image.open(uploaded_image))
        st.image(img, caption="Ảnh gốc đã tải lên", use_column_width=True)

        # Chỉ gọi lại Watershed nếu slider thay đổi
        if (
            st.session_state.get("prev_kernel_size") != kernel_size or
            st.session_state.get("prev_distance_thresh_factor") != distance_thresh_factor or
            st.session_state.get("prev_dilation_iterations") != dilation_iterations or
            st.session_state.get("prev_uploaded_image") != uploaded_image
        ):
            # Cập nhật giá trị cũ
            st.session_state.prev_kernel_size = kernel_size
            st.session_state.prev_distance_thresh_factor = distance_thresh_factor
            st.session_state.prev_dilation_iterations = dilation_iterations
            st.session_state.prev_uploaded_image = uploaded_image

            # Gọi Watershed và lưu kết quả
            st.session_state.processed_result = apply_watershed(img, kernel_size, distance_thresh_factor, dilation_iterations)

        # Hiển thị kết quả phân đoạn
        if st.session_state.processed_result is not None:
            st.image(st.session_state.processed_result, caption="Kết quả Watershed", use_column_width=True)

# Chạy ứng dụng
if __name__ == "__main__":
    run_app2()
