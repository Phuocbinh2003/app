import cv2
import numpy as np
import streamlit as st
from PIL import Image

def run_app3():
    st.title("Ứng dụng phát hiện khuôn mặt")

    # Tải lên ảnh
    uploaded_image = st.file_uploader("Tải lên một ảnh", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Đọc ảnh tải lên
        image = Image.open(uploaded_image)

        # Hiển thị ảnh đã tải lên
        st.image(image, caption="Ảnh đã tải lên", use_column_width=True)

        # Gọi hàm phát hiện khuôn mặt
        detect_faces_in_test_image(image)

def detect_faces_in_test_image(image):
    # Chuyển đổi ảnh PIL thành định dạng OpenCV (BGR)
    img = np.array(image.convert('RGB'))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # Chuyển đổi ảnh sang ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Sử dụng Haar Cascade để phát hiện khuôn mặt
    haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Vẽ bounding box quanh khuôn mặt
    for (x, y, w, h) in faces:
        face_region = gray[y:y+h, x:x+w]
        face_region_resized = cv2.resize(face_region, (24, 24)).flatten().reshape(1, -1)

        # Dự đoán bằng mô hình k-NN (giả sử có sẵn một mô hình đã được huấn luyện)
        # Ở đây bạn có thể gọi một hàm dự đoán từ mô hình k-NN của bạn nếu cần

        # Nếu khuôn mặt được phát hiện, vẽ bounding box
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Hiển thị ảnh với bounding box
    st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), caption="Kết quả phát hiện khuôn mặt", use_column_width=True)
