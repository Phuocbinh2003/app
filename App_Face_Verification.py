import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
from Face_Verification.yunet import YuNet
from Face_Verification.sface import SFace

# Valid combinations of backends and targets
backend_target_pairs = [
    [cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_TARGET_CPU],
]

backend_id = backend_target_pairs[0][0]
target_id = backend_target_pairs[0][1]

# Instantiate YuNet
face_detector = YuNet(
    modelPath="Face_Verification/face_detection_yunet_2023mar.onnx",
    inputSize=[320, 320],
    confThreshold=0.5,
    nmsThreshold=0.3,
    topK=5000,
    backendId=backend_id,
    targetId=target_id
)

# Instantiate SFace
face_recognizer = SFace(
    modelPath="Face_Verification/face_recognition_sface_2021dec.onnx",
    disType=0,  # cosine
    backendId=backend_id,
    targetId=target_id
)

def find_similar_faces(uploaded_image, folder_path):
    results = []
    # Chuyển đổi hình ảnh từ file uploader thành mảng NumPy
    image1 = Image.open(uploaded_image).convert("RGB")  # Chuyển đổi sang RGB
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)  # Chuyển đổi sang BGR

    face_detector.setInputSize([image1.shape[1], image1.shape[0]])
    faces1 = face_detector.infer(image1)

    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return []

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)
        if image2 is not None:  # Kiểm tra nếu ảnh được đọc thành công
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

# Streamlit UI
def run_app5():
    st.title("Face Recognition Application")
    uploaded_file = st.file_uploader("Upload a face image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        folder_path = 'Face_Verification/image'  # Adjust to your folder path
        similar_faces = find_similar_faces(uploaded_file, folder_path)

        if similar_faces:
            # Tìm file có độ chính xác cao nhất
            best_match = max(similar_faces, key=lambda x: x[1])  # x[1] là độ chính xác
            best_filename = best_match[0]
            best_score = best_match[1]

            st.write(f"File with highest accuracy: {best_filename}, Score: {best_score:.4f}")
            
            # Đọc file txt tương ứng
            student_info = read_student_info(best_filename, folder_path)
            st.write("Student Information:")
            st.write(student_info)
        else:
            st.write("No similar faces found.")

if __name__ == "__main__":
    run_app5()
