import streamlit as st
import cv2
import numpy as np
from yunet import YuNet
from sface import SFace
import matplotlib.pyplot as plt
from PIL import Image

# Valid combinations of backends and targets
backend_target_pairs = [
    [cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_TARGET_CPU],
    [cv2.dnn.DNN_BACKEND_CUDA,   cv2.dnn.DNN_TARGET_CUDA],
    [cv2.dnn.DNN_BACKEND_CUDA,   cv2.dnn.DNN_TARGET_CUDA_FP16],
    [cv2.dnn.DNN_BACKEND_TIMVX,  cv2.dnn.DNN_TARGET_NPU],
    [cv2.dnn.DNN_BACKEND_CANN,   cv2.dnn.DNN_TARGET_NPU]
]

backend_id = backend_target_pairs[0][0]
target_id = backend_target_pairs[0][1]

# Instantiate YuNet
face_detector = YuNet(modelPath="face_detection_yunet_2023mar.onnx",
                inputSize=[320, 320],
                confThreshold=0.5,
                nmsThreshold=0.3,
                topK=5000,
                backendId=backend_id,
                targetId=target_id)

# Instantiate SFace for face recognition
face_recognizer = SFace(modelPath="https://drive.google.com/uc?id=17XLFcW8RuUXP7ACj5z4SPLGXx8FudWhq",
                    disType=0,  # cosine
                    backendId=backend_id,
                    targetId=target_id)

def find_similar_faces(uploaded_image, folder_path):
    results = []
    image1 = cv2.cvtColor(np.array(uploaded_image), cv2.COLOR_RGB2BGR)
    face_detector.setInputSize([image1.shape[1], image1.shape[0]])
    faces1 = face_detector.infer(image1)

    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return []

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)
        face_detector.setInputSize([image2.shape[1], image2.shape[0]])
        faces2 = face_detector.infer(image2)

        if faces2.shape[0] > 0:
            result = face_recognizer.match(image1, faces1[0][:-1], image2, faces2[0][:-1])
            results.append((filename, result[0], result[1]))

    return results

# Streamlit UI
def run_app5():
    st.title("Face Recognition Application")
    uploaded_file = st.file_uploader("Upload a face image", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        folder_path = 'Face_Verification/image'  # Adjust to your folder path
        similar_faces = find_similar_faces(uploaded_file, folder_path)
    
        if similar_faces:
            st.write("Similar Faces:")
            for filename, score, match in similar_faces:
                st.write(f"File: {filename}, Score: {score:.4f}, Match: {'Yes' if match else 'No'}")
        else:
            st.write("No similar faces found.")
if __name__ == "__main__":
    run_app5()
