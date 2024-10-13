import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
from Face_Verification.yunet import YuNet
from Face_Verification.sface import SFace

# Define valid combinations of backends and targets
backend_target_pairs = [
    [cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_TARGET_CPU],
]

backend_id = backend_target_pairs[0][0]
target_id = backend_target_pairs[0][1]

# Instantiate YuNet for face detection
face_detector = YuNet(
    modelPath="Face_Verification/face_detection_yunet_2023mar.onnx",
    inputSize=[320, 320],
    confThreshold=0.5,
    nmsThreshold=0.3,
    topK=5000,
    backendId=backend_id,
    targetId=target_id
)

# Instantiate SFace for face recognition
face_recognizer = SFace(
    modelPath="Face_Verification/face_recognition_sface_2021dec.onnx",
    disType=0,  # cosine
    backendId=backend_id,
    targetId=target_id
)

def visualize_faces(image, results, box_color=(0, 255, 0), text_color=(0, 0, 255), fps=None):
    """Visualizes faces detected in an image."""
    output = image.copy()
    landmark_color = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 255), (0, 255, 255)]

    if fps is not None:
        cv2.putText(output, 'FPS: {:.2f}'.format(fps), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color)

    for det in results:
        bbox = det[0:4].astype(np.int32)
        cv2.rectangle(output, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), box_color, 2)
        conf = det[-1]
        cv2.putText(output, '{:.4f}'.format(conf), (bbox[0], bbox[1] + 12), cv2.FONT_HERSHEY_DUPLEX, 0.5, text_color)

        landmarks = det[4:14].astype(np.int32).reshape((5, 2))
        for idx, landmark in enumerate(landmarks):
            cv2.circle(output, landmark, 2, landmark_color[idx], 2)

    return output

def resize_image(image, target_size=(320, 239)):
    """Resizes the image to the specified target size while keeping the aspect ratio."""
    h, w = image.shape[:2]
    ratio = min(target_size[0] / h, target_size[1] / w)
    new_h, new_w = int(h * ratio), int(w * ratio)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # Create a padded image to maintain target size
    padded_image = np.zeros((target_size[0], target_size[1], 3), dtype=np.uint8)
    top = (target_size[0] - new_h) // 2
    left = (target_size[1] - new_w) // 2
    padded_image[top:top + new_h, left:left + new_w] = resized

    return padded_image

def run_app5():
    """Runs the Streamlit app."""
    st.title("Face Recognition App")

    # Part 1: Find student information from image
    st.header("Find Student Information from Image")
    uploaded_image = st.file_uploader("Upload Image...", type=["jpg", "jpeg", "png"], key="image")

    if uploaded_image is not None:
        folder_path = "Face_Verification/image"  # Path to the folder containing student images

        # Display uploaded image
        image1 = Image.open(uploaded_image).convert("RGB")
        image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
        st.image(image1, channels="BGR", caption="Uploaded Image", use_column_width=True)

        results = find_similar_faces(uploaded_image, folder_path)

        if results:
            st.subheader("Matched Faces:")
            for filename, score, _ in results:
                st.write(f"Image: {filename} - Score: {score:.4f}")
                student_info = read_student_info(filename, folder_path)
                st.write(f"Student Information: {student_info}")
        else:
            st.warning("No similar faces found.")

    # Part 2: Upload another image for comparison
    st.header("Upload Another Image for Comparison")
    uploaded_image2 = st.file_uploader("Upload Image for Comparison...", type=["jpg", "jpeg", "png"], key="image2")

    if uploaded_image2 is not None:
        image2 = Image.open(uploaded_image2).convert("RGB")
        image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
        st.image(image2, channels="BGR", caption="Comparison Image", use_column_width=True)

        if uploaded_image is not None:
            score = compare_faces(image1, image2)
            st.write(f"Similarity Score: {score:.4f}")

if __name__ == "__main__":
    run_app5()
