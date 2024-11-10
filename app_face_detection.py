import os
import cv2
import numpy as np
import joblib
import streamlit as st
from PIL import Image

# Function to compute Haar featur
def haar_features(img):
    integral_img = cv2.integral(img)
    haar_features = []

    # Vertical templates
    for i in range(0, img.shape[0] - 1):
        for j in range(0, img.shape[1] - 1):
            haar_value = (integral_img[i + 1, j + 1] - integral_img[i, j + 1] -
                          integral_img[i + 1, j] + integral_img[i, j])
            haar_features.append(haar_value)

    # Horizontal templates
    for i in range(0, img.shape[0] - 1):
        for j in range(0, img.shape[1] - 1):
            haar_value = (integral_img[i, j + 1] - integral_img[i + 1, j + 1] -
                          integral_img[i, j] + integral_img[i + 1, j])
            haar_features.append(haar_value)

    # Diagonal templates
    for i in range(0, img.shape[0] - 1):
        for j in range(0, img.shape[1] - 1):
            haar_value = (integral_img[i + 1, j + 1] - integral_img[i, j + 1] -
                          integral_img[i + 1, j] + integral_img[i, j])
            haar_features.append(haar_value)

    # Three-rectangle templates
    for i in range(0, img.shape[0] - 1):
        for j in range(0, img.shape[1] - 1):
            haar_value = (integral_img[i + 1, j] - integral_img[i, j] +
                          integral_img[i, j + 1] - integral_img[i + 1, j + 1])
            haar_features.append(haar_value)

    return np.array(haar_features)

# Function to resize an image
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

# Function for face detection using sliding window and Haar features
def sliding_window_haar_detect(img, model, window_size=(24, 24)):
    height, width = img.shape
    boxes = []
    step = 1  # Slide step of 1 pixel

    for y in range(0, height - window_size[1] + 1, step):
        for x in range(0, width - window_size[0] + 1, step):
            window = img[y:y + window_size[1], x:x + window_size[0]]
            if window.shape[0] == window_size[1] and window.shape[1] == window_size[0]:
                haar_feat = haar_features(window)  # Extract Haar features
                pred = model.predict([haar_feat])  # Predict using KNN
                if pred == 1:  # If face is detected
                    boxes.append((x, y, window_size[0], window_size[1]))  # Save box coordinates

    return boxes

def run_app3():
    st.title("1.Face and Non-Face Data")
    
    # Part 1: Display face and non-face images
    st.subheader("Face Images")
    face_image_paths = [
        'Face_Detection_folder/faces_24x24.png', 
    ]  # Add your actual image paths here
    for img_path in face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Face Image: {img_path}", use_column_width=True)

    st.subheader("Non-Face Images")
    non_face_image_paths = [
        'Face_Detection_folder/non_faces_24x24.png'
    ]  # Add your actual image paths here
    for img_path in non_face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Non-Face Image: {img_path}", use_column_width=True)

    # Part 2: Display training results and vector image
    st.title("2. Dataset test")
    face_image_paths = [
        'Face_Detection_folder/face_data1.png', 
        'Face_Detection_folder/face_data2.png',
    ]  # Add your actual image paths here
    for img_path in face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Face Image: {img_path}", use_column_width=True)

    st.title("3. Độ đo IoU")
    img = Image.open("Face_Detection_folder/iou_equation.png")
    st.image(img, caption="Độ đo IoU và công thức tính toán", use_column_width=True)
    
    st.write("""
        Độ đo **IoU (Intersection over Union)** là một chỉ số quan trọng trong các bài toán phát hiện và nhận diện đối tượng, dùng để đánh giá mức độ chồng lắp giữa hai hộp bao (bounding boxes): hộp dự đoán và hộp thực tế. IoU được tính bằng tỷ lệ diện tích giao nhau giữa hai hộp so với diện tích hợp nhất của chúng.
    
        Công thức tính IoU:
    """)
    
    # Hiển thị công thức với cú pháp LaTeX của Streamlit
    st.latex(r"IoU = \frac{\text{Diện tích giao nhau}}{\text{Diện tích hợp nhất}}")
    
    st.write("""
        Trong đó:
        - **Diện tích giao nhau** là phần diện tích mà hai hộp bao trùng nhau.
        - **Diện tích hợp nhất** là tổng diện tích của hai hộp trừ đi diện tích giao nhau.
    
        IoU có giá trị từ 0 đến 1:
        - **IoU = 0**: Không có phần giao nhau nào giữa hai hộp.
        - **IoU = 1**: Hai hộp trùng khớp hoàn toàn.
    
        Trong thực tế, một ngưỡng IoU (thường là 0.5 hoặc 0.7) được đặt ra để xác định xem một dự đoán có chính xác hay không. Nếu IoU giữa hộp dự đoán và hộp thực tế lớn hơn ngưỡng này, dự đoán được coi là đúng.
    """)
    

    
    st.title("Training Results")
    st.subheader("Vector Image")
    vector_image_paths = [
        'Face_Detection_folder/vecto.png'
    ]  # Add your actual image paths here
    for img_path in vector_image_paths:
        img = Image.open(img_path)
        st.image(img, caption="Vector Image", use_column_width=True)
    st.write("""
        - Haar Features là các đặc trưng hình ảnh được tính toán bằng cách thực hiện các phép toán tích phân giữa các vùng sáng và tối trong ảnh.
        - Vector đặc trưng là một đại diện số học của ảnh, được xây dựng từ các giá trị của Haar Features và có thể được sử dụng cho các thuật toán phân loại như KNN.
        - KNN được thử nghiệm với nhiều giá trị tham số k khác nhau để tìm ra giá trị k tối ưu.
    """)



    
    st.subheader("Training Chart")
    chart_image_paths = [
        'Face_Detection_folder/bieu_do.png'
    ]  # Add your actual image paths here
    for img_path in chart_image_paths:
        img = Image.open(img_path)
        st.image(img, caption="Training Chart", use_column_width=True)

    # Part 3: Display final result
    st.title("Kết quả")
    result_image_path = 'Face_Detection_folder/kq.png'  # Add your actual image path here
    result_image = Image.open(result_image_path)
    st.image(result_image, caption="Detection Result", use_column_width=True)




    
    st.title("Face Detection Application")
    st.write("Upload an image to detect faces.")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Read the image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Load the saved KNN model
        knn_model = joblib.load("knn_model.joblib")  # Ensure the model is in the same directory

        # Resize image and detect faces
        resized_img, new_w, new_h = resize_image(gray_image)
        boxes = sliding_window_haar_detect(resized_img, knn_model)

        # Tính tỷ lệ giữa ảnh gốc và ảnh đã resize
        scale_x = gray_image.shape[1] / new_w
        scale_y = gray_image.shape[0] / new_h

        # Vẽ box trên ảnh gốc với kích thước tương ứng
        for (x, y, w, h) in boxes:
            # Điều chỉnh tọa độ và kích thước box
            x_original = int(x * scale_x)
            y_original = int(y * scale_y)
            w_original = int(w * scale_x)
            h_original = int(h * scale_y)

            cv2.rectangle(image, (x_original, y_original), (x_original + w_original, y_original + h_original), (0, 255, 0), 1)

        # Display image with detection boxes
        st.image(image, channels="BGR", caption="Detected Faces")

# Main app where you can call run_app3()
if __name__ == "__main__":
    run_app3()
