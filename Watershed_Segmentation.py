import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image

# Hàm resize ảnh sao cho chiều cao bằng target_height
def resize_image(image, target_height):
    h, w = image.shape[:2]
    scaling_factor = target_height / h
    new_width = int(w * scaling_factor)
    resized_image = cv.resize(image, (new_width, target_height))
    return resized_image

# Hàm áp dụng Watershed
def apply_watershed(img, kernel_size, distance_thresh_factor, dilation_iterations):
    # Resize ảnh về 500x400
    img = cv.resize(img, (500, 400))

    # Chuyển sang ảnh xám và nhị phân Otsu
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Áp dụng phép mở rộng (Dilation)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated = cv.dilate(binary, kernel, iterations=dilation_iterations)

    # Distance transform
    dist_transform = cv.distanceTransform(dilated, cv.DIST_L2, 5)
    _, sure_fg = cv.threshold(dist_transform, distance_thresh_factor * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Tạo background và vùng chưa biết
    sure_bg = cv.dilate(sure_fg, kernel, iterations=5)
    unknown = cv.subtract(sure_bg, sure_fg)

    # Tạo markers
    _, markers = cv.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # Áp dụng Watershed
    markers = cv.watershed(img, markers)
    img[markers == -1] = [0, 0, 255]  # Đánh dấu biên bằng màu đỏ

    # Kết quả nhị phân (trắng trên nền đen)
    result_img = np.zeros_like(binary)
    contours, _ = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if h > 40 and w > 30:
            result_img[y:y+h, x:x+w] = binary[y:y+h, x:x+w]

    return result_img

# Chạy ứng dụng Streamlit
def run_app2():
    st.title("✨ Ứng dụng phân đoạn ký tự biển số ✨")

    # Phần 1: Hiển thị ảnh mẫu và kết quả
    st.header("1. Ảnh mẫu và kết quả")
    st.image("my_folder/train_test.png", caption="Ảnh mẫu", use_column_width=True)
    st.image("my_folder/cb.png", caption="Các bước Watershed", use_column_width=True)

    # Phần 2: Tải ảnh và xử lý
    st.header("2. Tải ảnh và phân đoạn ký tự")
    uploaded_image = st.file_uploader("Tải ảnh biển số lên", type=["jpg", "png", "jpeg"])

    # Sidebar tùy chỉnh tham số
    st.sidebar.header("Tùy chỉnh tham số Watershed")
    kernel_size = st.sidebar.slider("Kích thước kernel", 1, 15, 3, 1)
    distance_thresh_factor = st.sidebar.slider("Ngưỡng Distance Transform", 0.1, 1.0, 0.3, 0.1)
    dilation_iterations = st.sidebar.slider("Số lần Dilation", 1, 10, 3, 1)

    # Khởi tạo session_state nếu chưa tồn tại
    if "processed_result" not in st.session_state:
        st.session_state.processed_result = None
        st.session_state.prev_params = {"kernel_size": None, "distance_thresh_factor": None, "dilation_iterations": None}

    if uploaded_image:
        img = np.array(Image.open(uploaded_image))
        st.image(img, caption="Ảnh gốc", use_column_width=True)

        params = {
            "kernel_size": kernel_size,
            "distance_thresh_factor": distance_thresh_factor,
            "dilation_iterations": dilation_iterations,
        }

        # Kiểm tra nếu tham số thay đổi hoặc chưa xử lý
        if st.session_state.processed_result is None or st.session_state.prev_params != params:
            st.session_state.processed_result = apply_watershed(img, kernel_size, distance_thresh_factor, dilation_iterations)
            st.session_state.prev_params = params

        st.image(st.session_state.processed_result, caption="Kết quả Watershed", use_column_width=True)

if __name__ == "__main__":
    run_app2()
