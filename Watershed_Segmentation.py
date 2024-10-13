import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image
import os

# Hàm để resize ảnh sao cho chiều cao của chúng bằng nhau
def resize_image(image, target_height):
    h, w = image.shape[:2]
    scaling_factor = target_height / h
    new_width = int(w * scaling_factor)
    resized_image = cv.resize(image, (new_width, target_height))
    return resized_image

# Hàm để áp dụng Watershed với tham số động
def apply_watershed(img, kernel_size, distance_thresh_factor, dilation_iterations):
    # Resize ảnh về 500x400
    img = cv.resize(img, (500, 400))

    # Chuyển sang ảnh xám và nhị phân Otsu
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

    # Bước 1: Áp dụng phép mở rộng (Dilation)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    dilated = cv.dilate(binary, kernel, iterations=dilation_iterations)

    # Bước 2: Distance transform
    dist_transform = cv.distanceTransform(dilated, cv.DIST_L2, 5)

    # Bước 3: Ngưỡng hóa ảnh distance transform với hệ số distance_thresh_factor
    _, sure_fg = cv.threshold(dist_transform, distance_thresh_factor * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # Bước 4: Tạo background bằng phép giãn nở (dilation)
    sure_bg = cv.dilate(sure_fg, kernel, iterations=5)

    # Bước 5: Tìm vùng chưa biết (unknown region)
    unknown = cv.subtract(sure_bg, sure_fg)

    # Bước 6: Tạo markers cho watershed
    _, markers = cv.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    # Bước 7: Áp dụng thuật toán Watershed
    img_markers = img.copy()
    cv.watershed(img_markers, markers)
    img_markers[markers == -1] = [0, 0, 255]  # Đánh dấu biên với màu đỏ

    # Hiển thị kết quả các ký tự màu trắng trên nền đen
    result_img = np.zeros_like(binary)
    contours, _ = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if h > 40 and w > 30:
            result_img[y:y+h, x:x+w] = binary[y:y+h, x:x+w]

    return result_img

# Hàm cho ứng dụng
def run_app2():
    st.title('✨ Ứng dụng phân đoạn ký tự biển số ✨')

    # Thêm input để nhập các tham số
    st.sidebar.header("Tùy chỉnh tham số Watershed")
    kernel_size = st.sidebar.slider("Kích thước kernel", min_value=1, max_value=15, value=3, step=1)
    distance_thresh_factor = st.sidebar.slider("Ngưỡng Distance Transform", min_value=0.1, max_value=1.0, value=0.3, step=0.1)
    dilation_iterations = st.sidebar.slider("Số lần Dilation", min_value=1, max_value=10, value=3, step=1)

    # Phần 3: Tải ảnh lên và phân đoạn ký tự
    st.header("3. Tải ảnh lên và phân đoạn ký tự")
    
    uploaded_image = st.file_uploader("Tải ảnh biển số lên", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        # Đọc ảnh từ người dùng tải lên
        img = np.array(Image.open(uploaded_image))
        st.image(img, caption='Ảnh đã tải lên', use_column_width=True)

        # Áp dụng thuật toán Watershed với tham số nhập vào
        result = apply_watershed(img, kernel_size, distance_thresh_factor, dilation_iterations)

        # Hiển thị kết quả
        st.image(result, caption='Kết quả phân đoạn Watershed', use_column_width=True)

if __name__ == "__main__":
    run_app2()
