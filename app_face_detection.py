import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


# Hàm trích xuất đặc trưng Haar
def haar_features(img):
    integral_img = cv2.integral(img)
    haar_features = []

    # Mẫu dọc
    for i in range(0, img.shape[0] - 1):
        for j in range(0, img.shape[1] - 1):
            haar_value = (integral_img[i + 1, j + 1] - integral_img[i, j + 1] -
                          integral_img[i + 1, j] + integral_img[i, j])
            haar_features.append(haar_value)

    return np.array(haar_features)


# Hàm resize ảnh
def resize_image(image, target_size=100):
    h, w = image.shape[:2]
    if w > h:
        new_w = target_size
        new_h = int(h * (target_size / w))
    else:
        new_h = target_size
        new_w = int(w * (target_size / h))

    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    return resized_image, new_w, new_h  # Return the new dimensions


# Hàm sử dụng cửa sổ trượt để phát hiện khuôn mặt
def sliding_window_haar_detect(img, model, window_size=(24, 24)):
    height, width = img.shape
    boxes = []

    step = 1  # Bước trượt 1 pixel

    for y in range(0, height - window_size[1] + 1, step):
        for x in range(0, width - window_size[0] + 1, step):
            window = img[y:y + window_size[1], x:x + window_size[0]]
            if window.shape[0] == window_size[1] and window.shape[1] == window_size[0]:
                haar_feat = haar_features(window)  # Trích xuất đặc trưng Haar
                pred = model.predict([haar_feat])  # Dự đoán bằng KNN
                if pred == 1:  # Nếu phát hiện khuôn mặt
                    boxes.append((x, y, window_size[0], window_size[1]))  # Lưu tọa độ box

    return boxes


def run_app3():
    # Part 1: Upload and process image
    st.title("Face Detection App")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        # Đọc ảnh từ file tải lên
        test = Image.open(uploaded_file)
        test = np.array(test.convert('RGB'))  # Chuyển ảnh sang định dạng RGB
        
        # Hiển thị ảnh gốc
        st.image(test, caption="Uploaded Image", use_column_width=True)

        # Resize ảnh
        resized_img, new_w, new_h = resize_image(test)
        st.image(resized_img, caption="Resized Image", use_column_width=True)

        # Sử dụng mô hình KNN giả định (phải được train từ trước)
        knn_model = KNeighborsClassifier(n_neighbors=3)  # Load hoặc train model trước khi dùng

        # Phát hiện khuôn mặt bằng cửa sổ trượt
        boxes = sliding_window_haar_detect(resized_img, knn_model)

        # Vẽ các box phát hiện lên ảnh gốc
        result_img = test.copy()
        for (x, y, w, h) in boxes:
            # Chuyển đổi tọa độ từ ảnh resized sang ảnh gốc
            orig_x = int(x * (test.shape[1] / new_w))
            orig_y = int(y * (test.shape[0] / new_h))
            orig_w = int(w * (test.shape[1] / new_w))
            orig_h = int(h * (test.shape[0] / new_h))

            cv2.rectangle(result_img, (orig_x, orig_y), (orig_x + orig_w, orig_y + orig_h), (0, 255, 0), 2)

        # Hiển thị kết quả
        st.image(result_img, caption="Detection Result", use_column_width=True)


# Main app
if __name__ == "__main__":
    run_app3()
