import gdown
import os
import streamlit as st
import cv2
import numpy as np
from yunet import YuNet
from sface import SFace
import matplotlib.pyplot as plt

# Tải model từ Google Drive
model_url = 'https://drive.google.com/uc?id=17XLFcW8RuUXP7ACj5z4SPLGXx8FudWhq'
output_model_path = 'face_recognition_sface_2021dec.onnx'

# Kiểm tra xem model đã tồn tại chưa
if not os.path.exists(output_model_path):
    gdown.download(model_url, output_model_path, quiet=False)

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
face_recognizer = SFace(modelPath=output_model_path,
                        disType=0,  # cosine
                        backendId=backend_id,
                        targetId=target_id)

def visualize_matches(img1, faces1, img2, faces2, matches, scores):
    out1 = img1.copy()
    out2 = img2.copy()
    matched_box_color = (0, 255, 0)    # BGR
    mismatched_box_color = (0, 0, 255)  # BGR

    # Draw bbox for the first image
    draw_bounding_box(out1, faces1[0][:4], matched_box_color)

    # Draw bounding boxes for the second image
    for index, match in enumerate(matches):
        draw_bounding_box(out2, faces2[index][:4], matched_box_color if match else mismatched_box_color)

    return np.concatenate([out1, out2], axis=1)

def draw_bounding_box(image, bbox, color):
    x, y, w, h = bbox.astype(np.int32)
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

# Streamlit UI
st.title("Face Recognition App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image2 = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Detect faces in the uploaded image
    face_detector.setInputSize([image2.shape[1], image2.shape[0]])
    faces2 = face_detector.infer(image2)
    assert faces2.shape[0] > 0, 'Cannot find a face in the uploaded image.'

    # Load a reference image (You can change this)
    img1_path = "path/to/your/reference/image.jpg"  # Thay đổi đường dẫn đến ảnh tham chiếu
    image1 = cv2.imread(img1_path)

    # Detect faces in the reference image
    face_detector.setInputSize([image1.shape[1], image1.shape[0]])
    faces1 = face_detector.infer(image1)
    assert faces1.shape[0] > 0, 'Cannot find a face in the reference image.'

    # Match faces
    scores = []
    matches = []
    for face in faces2:
        result = face_recognizer.match(image1, faces1[0][:-1], image2, face[:-1])
        scores.append(result[0])
        matches.append(result[1])

    # Draw and visualize results
    image = visualize_matches(image1, faces1, image2, faces2, matches, scores)
    st.image(image, channels="BGR", caption="Matched Faces")
