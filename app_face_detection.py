import streamlit as st
import joblib
import cv2
import numpy as np
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier

# Load the trained KNN model
def load_knn_model(model_path):
    return joblib.load(model_path)

# Preprocess image for KNN model (resize, grayscale, etc.)
def preprocess_image_for_detection(img, width=100):
    img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)  # Convert PIL image to grayscale
    aspect_ratio = img_gray.shape[1] / img_gray.shape[0]  # W/H ratio
    new_height = int(width / aspect_ratio)
    resized_img = cv2.resize(img_gray, (width, new_height))  # Resize image
    smoothed_img = cv2.GaussianBlur(resized_img, (5, 5), 0)  # Apply Gaussian smoothing
    return smoothed_img, img.size  # Return resized and original size

# Haar feature extraction function (same as in your previous code)
def haar_features(img):
    integral_img = cv2.integral(img)
    haar_features = []

    # Example Haar-like feature extraction (modify as needed)
    for i in range(0, img.shape[0] - 1):
        for j in range(0, img.shape[1] - 1):
            haar_value = (integral_img[i + 1, j + 1] - integral_img[i, j + 1] - integral_img[i + 1, j] + integral_img[i, j])
            haar_features.append(haar_value)

    return np.array(haar_features)

# Perform face detection using sliding window with the KNN model
def sliding_window_haar_detect(img, model, window_size=(24, 24)):
    height, width = img.shape
    boxes = []
    step = 1  # Sliding step in pixels

    for y in range(0, height - window_size[1] + 1, step):
        for x in range(0, width - window_size[0] + 1, step):
            window = img[y:y + window_size[1], x:x + window_size[0]]
            if window.shape[0] == window_size[1] and window.shape[1] == window_size[0]:
                haar_feat = haar_features(window)  # Extract Haar features
                pred = model.predict([haar_feat])  # Predict with KNN model
                if pred == 1:  # If face is detected
                    boxes.append((x, y, window_size[0], window_size[1]))  # Store box coordinates

    return boxes

# Rescale bounding boxes back to the original image size
def rescale_boxes(boxes, original_size, resized_size):
    original_w, original_h = original_size
    resized_w, resized_h = resized_size
    scale_x = original_w / resized_w
    scale_y = original_h / resized_h
    scaled_boxes = [(int(x * scale_x), int(y * scale_y), int(w * scale_x), int(h * scale_y)) for (x, y, w, h) in boxes]
    return scaled_boxes

def run_app3():
    # Part 1: Display face and non-face images
    st.title("Face and Non-face Data")
    
    st.subheader("Face Images")
    face_image_paths = ['Face_Detection_folder/faces_24x24.png']  # Add your actual image paths here
    for img_path in face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Face Image: {img_path}", use_column_width=True)

    st.subheader("Non-Face Images")
    non_face_image_paths = ['Face_Detection_folder/non_faces_24x24.png']  # Add your actual image paths here
    for img_path in non_face_image_paths:
        img = Image.open(img_path)
        st.image(img, caption=f"Non-Face Image: {img_path}", use_column_width=True)

    # Part 2: Display training results and vector image
    st.title("Training Results")
    st.subheader("Train Vector Image")
    vector_image_path = 'Face_Detection_folder/vecto.png'  # Add your actual image path here
    vector_image = Image.open(vector_image_path)
    st.image(vector_image, caption="Training Vector", use_column_width=True)

    st.subheader("Training Chart")
    chart_image_path = 'Face_Detection_folder/bieu_do.png'  # Add your actual image path here
    chart_image = Image.open(chart_image_path)
    st.image(chart_image, caption="Training Chart", use_column_width=True)

    # Part 3: Face Detection with KNN model
    st.title("Face Detection Using KNN Model")

    # Upload image for face detection
    uploaded_image = st.file_uploader("Upload an image for face detection", type=["jpg", "png", "jpeg"])
    
    if uploaded_image is not None:
        # Load and preprocess the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Preprocess the uploaded image
        resized_img, original_size = preprocess_image_for_detection(image)

        # Load the KNN model
        knn_model = load_knn_model('knn_model.joblib')

        # Perform face detection using sliding window
        boxes = sliding_window_haar_detect(resized_img, knn_model)

        # Rescale bounding boxes back to the original image size
        scaled_boxes = rescale_boxes(boxes, original_size, resized_img.shape)

        # Draw bounding boxes on the original image
        result_img = np.array(image).copy()
        for (x, y, w, h) in scaled_boxes:
            cv2.rectangle(result_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display the final result with bounding boxes
        st.image(result_img, caption="Detection Result", use_column_width=True)

# Main app
if __name__ == "__main__":
    run_app3()
