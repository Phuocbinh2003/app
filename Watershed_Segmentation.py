import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image
import os

# Hàm để resize ảnh sao cho chiều cao của chúng bằng nha
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

    # Đường dẫn tới các hình ảnh phần 

    # Phần 1: Hiển thị cho 2 cặp ảnh đầu tiên (theo hàng dọc)
    st.header("1. Ảnh Train và Kết quả")

   
    img_step_1 = cv.imread("my_folder/train_test.png")
    st.image(img_step_1, caption='', use_column_width=True)
  
    st.header("1. Các bước của Watershed")

   
    img_step_1 = cv.imread("my_folder/cb.png")
    st.image(img_step_1, caption='', use_column_width=True)
    st.write("""
    1. **Chuyển ảnh sang ảnh xám và nhị phân (Otsu thresholding):**
    
        Ảnh đầu vào được chuyển sang ảnh xám để dễ dàng xử lý. Sau đó, sử dụng phương pháp thresholding Otsu để chuyển ảnh xám thành ảnh nhị phân. Phương pháp này giúp phân biệt rõ các đối tượng với nền trong ảnh.
    
    2. **Áp dụng phép mở rộng (Dilation):**
    
        Phép mở rộng được áp dụng với một kernel hình vuông để làm tăng kích thước của các đối tượng trong ảnh nhị phân. Mục tiêu là làm mịn các biên và tăng cường các đối tượng nhỏ.
    
    3. **Tính toán Distance Transform:**
    
        Sử dụng hàm `cv.distanceTransform` để tính toán ảnh distance transform. Quá trình này giúp xác định khoảng cách từ các pixel nền tới các biên giới của các đối tượng, tạo ra một bản đồ thể hiện độ xa của mỗi điểm từ biên.
    
    4. **Ngưỡng hóa Distance Transform:**
    
        Áp dụng ngưỡng (thresholding) trên ảnh distance transform với một hệ số (`distance_thresh_factor`) để xác định vùng foreground (đối tượng) chắc chắn. Vùng này sẽ được phân loại là các đối tượng trong ảnh.
    
        Tiếp theo, dùng phép giãn nở (dilation) để tạo ra ảnh background, giúp xác định các vùng nền trong ảnh.
    
    5. **Tìm vùng chưa biết (Unknown regions):**
    
        Vùng chưa biết được xác định bằng cách lấy hiệu giữa background và foreground chắc chắn. Những vùng này chưa thể xác định rõ là đối tượng hay nền, nên sẽ được đánh dấu là vùng chưa biết.
    
    6. **Tạo markers cho Watershed:**
    
        Sử dụng hàm `cv.connectedComponents` để tạo các markers từ vùng foreground chắc chắn. Các vùng chưa biết được gán giá trị marker là 0, còn vùng background được gán giá trị là 1. Các markers này sẽ được sử dụng trong thuật toán Watershed.
    
    7. **Áp dụng thuật toán Watershed:**
    
        Thuật toán Watershed được áp dụng với các markers đã tạo. Thuật toán này phân chia ảnh thành các vùng khác nhau dựa trên các marker, giúp tách các đối tượng trong ảnh. Biên của các vùng sẽ được đánh dấu bằng màu đỏ `[0, 0, 255]`.
    
    8. **Tìm các contours và hiển thị kết quả:**
    
        Sử dụng hàm `cv.findContours` để tìm các contours trong ảnh đã qua dilation. Các contours này đại diện cho các biên của các đối tượng trong ảnh.
    
        Sau đó, lọc các contours theo kích thước (chiều cao và chiều rộng) để chỉ giữ lại những đối tượng có kích thước hợp lý. Kết quả là một ảnh với các ký tự màu trắng trên nền đen, thể hiện các đối tượng đã được phân vùng. Ảnh này sẽ được hiển thị với matplotlib.
    """)






    # Phần 3: Tải ảnh lên và phân đoạn ký tự
    st.sidebar.header("Tùy chỉnh tham số Watershed")
    kernel_size = st.sidebar.slider("Kích thước kernel", min_value=1, max_value=15, value=3, step=1)
    distance_thresh_factor = st.sidebar.slider("Ngưỡng Distance Transform", min_value=0.1, max_value=1.0, value=0.3, step=0.1)
    dilation_iterations = st.sidebar.slider("Số lần Dilation", min_value=1, max_value=10, value=3, step=1)

    # Phần 3: Tải ảnh lên và phân đoạn ký tự
    st.header("2. Tải ảnh lên và phân đoạn ký tự")
    
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
