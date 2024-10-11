import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Hàm xử lý hình ảnh trong ứng dụng 2
def process_image(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv.dilate(binary, kernel, iterations=1)
    dist_transform = cv.distanceTransform(dilated, cv.DIST_L2, 5)
    _, sure_fg = cv.threshold(dist_transform, 0.3 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)
    sure_bg = cv.dilate(dilated, kernel, iterations=2)
    unknown = cv.subtract(sure_bg, sure_fg)
    _, markers = cv.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0
    img_watershed = image.copy()
    cv.watershed(img_watershed, markers)
    img_watershed[markers == -1] = [0, 0, 255]

    contours, _ = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    char_images = []
    image_with_boxes = image.copy()

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        if h > 7 and w > 7 and h < 100 and w < 100:
            cv.rectangle(image_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 1)
            char_image = binary[y:y+h, x:x+w]
            char_images.append(char_image)

    return binary, dilated, img_watershed, image_with_boxes, char_images

# Hàm cho ứng dụng thứ 2
def run_app2():
    st.title('✨ Ứng dụng phân đoạn ký tự biển số ✨')

    # Danh sách các đường dẫn tới các hình ảnh train và test
    train_image_paths = [
        "my_folder/Buoc_test1.png",
        "my_folder/Buoc_test2.png"
    ]
    
    test_image_paths = [
        "my_folder/KQ_test1.png",
        "my_folder/KQ_test2.png"
    ]

    # Hiển thị lần lượt ảnh train và kết quả
    st.header("1. Ảnh Train và Kết quả")

    for train_image_path in train_image_paths:
        # Đọc ảnh từ đường dẫn
        img_np = cv.imread(train_image_path)

        if img_np is not None:
            st.image(img_np, caption='Train Image', use_column_width=True)

            binary, dilated, img_watershed, image_with_boxes, char_images = process_image(img_np)

            # Hiển thị kết quả
            fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
            axes[0].imshow(binary, cmap='gray')
            axes[0].set_title('Binarization')
            axes[1].imshow(cv.cvtColor(img_watershed, cv.COLOR_BGR2RGB))
            axes[1].set_title('Watershed Segmentation')
            axes[2].imshow(cv.cvtColor(image_with_boxes, cv.COLOR_BGR2RGB))
            axes[2].set_title('Bounding Boxes')

            for ax in axes:
                ax.axis('off')
            
            st.pyplot(fig)

            st.subheader("Ký tự phát hiện được")
            cols = st.columns(len(char_images))
            for idx, char_img in enumerate(char_images):
                with cols[idx]:
                    st.image(char_img, caption=f"Ký tự {idx + 1}", channels="GRAY")

    # Hiển thị lần lượt ảnh test
    st.header("2. Ảnh Test")

    for test_image_path in test_image_paths:
        # Đọc ảnh từ đường dẫn
        img_np = cv.imread(test_image_path)

        if img_np is not None:
            st.image(img_np, caption='Test Image', use_column_width=True)

    # Phần dòng chữ tùy chọn
    st.header("3. Nhập dòng chữ của bạn")
    user_text = st.text_input("Nhập nội dung:")
    if user_text:
        st.write(f"Bạn đã nhập: {user_text}")

    # Phần upload ảnh và thực hiện Watershed
    st.header("4. Upload và Thực hiện Watershed")

    uploaded_file = st.file_uploader("Chọn một hình ảnh", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_np = cv.imdecode(file_bytes, 1)

        if img_np is not None:
            st.image(img_np, caption='Uploaded Image', use_column_width=True)
            binary, dilated, img_watershed, image_with_boxes, char_images = process_image(img_np)

            st.write("### Processing")
            fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
            axes[0].imshow(binary, cmap='gray')
            axes[0].set_title('Binarization')
            axes[1].imshow(cv.cvtColor(img_watershed, cv.COLOR_BGR2RGB))
            axes[1].set_title('Watershed Segmentation')
            axes[2].imshow(cv.cvtColor(image_with_boxes, cv.COLOR_BGR2RGB))
            axes[2].set_title('Bounding Boxes')

            for ax in axes:
                ax.axis('off')

            st.pyplot(fig)
