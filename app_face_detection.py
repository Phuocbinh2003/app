import os
import cv2
import numpy as np
import joblib  # Library for loading the model
import streamlit as st
from PIL import Image

# Load the KNN model
def load_model(model_path):
    return joblib.load(model_path)

# Function to extract Haar features
def haar_features(img):
    integral_img = cv2.integral(img)
    haar_features = []

    # Vertical pattern
    for i in range(0, img.shape[0] - 1):
        for j in range(0, img.shape[1] - 1):
            haar_value = (integral_img[i + 1, j + 1] - integral_img[i, j + 1] -
                          integral_img[i + 1, j] + integral_img[i, j])
            haar_features.append(haar_value)

    # Horizontal pattern
    for i in range(0, img.shape[0] - 1):
        for j in range(0, img.shape[1] - 1):
            haar_value = (integral_img[i, j + 1] - integral_img[i + 1, j + 1] -
                          integral_img[i, j] + integral_img[i + 1, j])
            haar_features.append(haar_value)

    return np.array(haar_features)

# Sliding window Haar detection
def sliding_window_haar_detect(img, model, window_size=(24, 24)):
    height, width = img.shape
    boxes = []
    step = 1  # Step size for sliding window

    for y in range(0, height - window_size[1] + 1, step):
        for x in range(0, width - window_size[0] + 1, step):
            window = img[y:y + window_size[1], x:x + window_size[0]]
            if window.shape[0] == window_size[1] and window.shape[1] == window_size[0]:
                haar_feat = haar_features(window)
                pred = model.predict([haar_feat])  # Predict using KNN
                if pred == 1:  # If face detected
                    boxes.append((x, y, window_size[0], window_size[1]))

    return boxes

# Main application function
def run_app3():
    st.title("Face Detection with KNN")

    # Load the KNN model
    model_path = "knn_model.joblib"  # Update with your model path
    model = load_model(model_path)

    # Image upload
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(uploaded_file)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)  # Convert to grayscale

        # Resize image for processing
        img = cv2.resize(img, (100, int(img.shape[0] * (100 / img.shape[1]))))

        # Perform sliding window detection
        boxes = sliding_window_haar_detect(img, model)

        # Draw boxes on the image
        for (x, y, w, h) in boxes:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)

        # Convert the result image to display
        result_image = Image.fromarray(img)
        st.image(result_image, caption="Detection Result", use_column_width=True)

if __name__ == "__main__":
    run_app3()
