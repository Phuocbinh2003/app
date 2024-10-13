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

# Hàm để áp dụng Watershed
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

    # Đường dẫn tới các hình ảnh phần 1
    step_image_path_1 = "my_folder/Buoc_test1.png"
    result_image_path_1 = "my_folder/KQ_test1.png"

    step_image_path_2 = "my_folder/Buoc_test2.png"
    result_image_path_2 = "my_folder/KQ_test2.png"

    # Phần 1: Hiển thị cho 2 cặp ảnh đầu tiên (theo hàng dọc)
    st.header("1. Ảnh Train và Kết quả")

    st.write("### Các bước Watershed")
    if os.path.exists(step_image_path_1):
        img_step_1 = cv.imread(step_image_path_1)
        if img_step_1 is not None:
            st.image(img_step_1, caption='', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {step_image_path_1}")

    st.write("### Kết quả 1")
    if os.path.exists(result_image_path_1):
        img_result_1 = cv.imread(result_image_path_1)
        if img_result_1 is not None and img_step_1 is not None:
            img_result_1_resized = resize_image(img_result_1, img_step_1.shape[0])
            st.image(img_result_1_resized, caption='', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {result_image_path_1}")

    st.write("### Các bước Watershed")
    if os.path.exists(step_image_path_2):
        img_step_2 = cv.imread(step_image_path_2)
        if img_step_2 is not None:
            st.image(img_step_2, caption='', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {step_image_path_2}")

    st.write("### Kết quả 2")
    if os.path.exists(result_image_path_2):
        img_result_2 = cv.imread(result_image_path_2)
        if img_result_2 is not None and img_step_2 is not None:
            img_result_2_resized = resize_image(img_result_2, img_step_2.shape[0])
            st.image(img_result_2_resized, caption='Kết quả', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {result_image_path_2}")

    # Đường dẫn tới các hình ảnh phần 2 (chỉ 2 ảnh)
    step_image_path_3 = "my_folder/KQ1.png"
    result_image_path_3 = "my_folder/KQ2.png"
    st.text("Sử dụng grid_search để tìm kiếm thông số phân đoạn ký tự khá tốt")
    st.text("Thông số tốt nhất tìm kiếm được là")
    st.text("kernel_size = 3 ")
    st.text("distance_thresh_factor = 0.3 ")
    st.text("dilation_iterations = 3")

    # Phần 2: Hiển thị cho 1 cặp ảnh tiếp theo (theo hàng dọc)
    st.header("2. Ảnh Test và Kết quả")

    st.write("### Kết quả 1")
    if os.path.exists(step_image_path_3):
        img_step_3 = cv.imread(step_image_path_3)
        if img_step_3 is not None:
            st.image(img_step_3, caption='', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {step_image_path_3}")

    st.write("### Kết quả 2")
    if os.path.exists(result_image_path_3):
        img_result_3 = cv.imread(result_image_path_3)
        if img_result_3 is not None and img_step_3 is not None:
            img_result_3_resized = resize_image(img_result_3, img_step_3.shape[0])
            st.image(img_result_3_resized, caption='', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {result_image_path_3}")

    # Phần 3: Tải ảnh lên và phân đoạn ký tự
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
