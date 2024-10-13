import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
from Face_Verification.yunet import YuNet
from Face_Verification.sface import SFace

# Initialize face detector and recognizer
backend_id = cv2.dnn.DNN_BACKEND_OPENCV
target_id = cv2.dnn.DNN_TARGET_CPU

face_detector = YuNet(
    modelPath="Face_Verification/face_detection_yunet_2023mar.onnx",
    inputSize=[320, 320],
    confThreshold=0.5,
    nmsThreshold=0.3,
    topK=5000,
    backendId=backend_id,
    targetId=target_id
)

face_recognizer = SFace(
    modelPath="Face_Verification/face_recognition_sface_2021dec.onnx",
    disType=0,  # cosine
    backendId=backend_id,
    targetId=target_id
)

def resize_image(image, width=320, height=239):
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)

def find_similar_faces(uploaded_image, folder_path):
    results = []
    image1 = Image.open(uploaded_image).convert("RGB")
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    image1 = resize_image(image1)

    face_detector.setInputSize([image1.shape[1], image1.shape[0]])
    faces1 = face_detector.infer(image1)

    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return []

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)

        if image2 is not None:
            image2 = resize_image(image2)
            face_detector.setInputSize([image2.shape[1], image2.shape[0]])
            faces2 = face_detector.infer(image2)

            if faces2.shape[0] > 0:
                result = face_recognizer.match(image1, faces1[0][:-1], image2, faces2[0][:-1])
                results.append((filename, result[0], result[1]))

    return results

def read_student_info(filename, folder_path):
    txt_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.txt")
    if os.path.exists(txt_file_path):
        with open(txt_file_path, "r") as f:
            return f.read()
    else:
        return "No student information found."

def compare_faces(image1, image2):
    faces1 = face_detector.infer(image1)
    faces2 = face_detector.infer(image2)

    if faces1.shape[0] == 0 or faces2.shape[0] == 0:
        return 0.0

    result = face_recognizer.match(image1, faces1[0][:-1], image2, faces2[0][:-1])
    return result[0]

def run_app5():
    st.title("Face Recognition App")

    # Part 1: Find student information from image
    st.header("Find Student Information from Image")
    uploaded_image = st.file_uploader("Upload Image...", type=["jpg", "jpeg", "png"], key="image")

    if uploaded_image is not None:
        folder_path = "Face_Verification/image"
        results = find_similar_faces(uploaded_image, folder_path)

        if results:
            best_match = max(results, key=lambda x: x[1])
            best_filename, best_score, _ = best_match

            best_image_path = os.path.join(folder_path, best_filename)
            best_image = cv2.imread(best_image_path)
            best_image = resize_image(best_image)

            detected_faces = face_detector.infer(best_image)
            if detected_faces.shape[0] > 0:
                st.image(best_image, caption="Best Match with Detected Faces", use_column_width=True)
            else:
                st.warning("No face detected in the best matching image.")

            student_info = read_student_info(best_filename, folder_path)
            st.write(f"**Matched File:** {best_filename}")
            st.write(f"**Score:** {best_score:.2f}")
            st.write(f"**Student Info:** {student_info}")
        else:
            st.warning("No matches found.")

    # Part 2: Compare portrait and ID photo
    st.header("Compare Portrait and ID Photo")
    uploaded_image1 = st.file_uploader("Upload Portrait Image...", type=["jpg", "jpeg", "png"], key="portrait")
    uploaded_image2 = st.file_uploader("Upload ID Image...", type=["jpg", "jpeg", "png"], key="id")

    if uploaded_image1 and uploaded_image2:
        image1 = Image.open(uploaded_image1).convert("RGB")
        image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)

        image2 = Image.open(uploaded_image2).convert("RGB")
        image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)

        image1 = resize_image(image1)
        image2 = resize_image(image2)

        score = compare_faces(image1, image2)
        st.success(f"Similarity Score: {score:.2f}")

        if score > 0.5:
            st.success("The images belong to the same person.")
        else:
            st.warning("The images do not belong to the same person.")

if __name__ == "__main__":
    run_app5()
