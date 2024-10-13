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

    # Store detected face coordinates for later use
    face_bboxes = []
    
    for det in results:
        bbox = det[0:4].astype(np.int32)
        cv2.rectangle(output, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), box_color, 2)
        conf = det[-1]
        cv2.putText(output, '{:.4f}'.format(conf), (bbox[0], bbox[1] + 12), cv2.FONT_HERSHEY_DUPLEX, 0.5, text_color)

        landmarks = det[4:14].astype(np.int32).reshape((5, 2))
        for idx, landmark in enumerate(landmarks):
            cv2.circle(output, landmark, 2, landmark_color[idx], 2)
        
        # Append the bounding box to the list
        face_bboxes.append(bbox)

    return output, face_bboxes

def resize_image(image, target_size=320):
    """Resizes the image while maintaining the aspect ratio."""
    h, w, _ = image.shape
    if w > h:
        new_w = target_size
        new_h = int(h * (target_size / w))  # Calculate new height based on width
    else:
        new_h = target_size
        new_w = int(w * (target_size / h))  # Calculate new width based on height

    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    return resized_image, new_w, new_h  # Return resized image and new dimensions

def read_student_info(filename, folder_path):
    """Reads student information from a text file associated with the image."""
    txt_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.txt")
    if os.path.exists(txt_file_path):
        with open(txt_file_path, "r") as f:
            return f.read()
    return "No student information found."

def find_similar_faces(uploaded_image, folder_path):
    """Finds similar faces in a folder based on the uploaded image."""
    results = []
    image1 = Image.open(uploaded_image).convert("RGB")
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    image1_resized, new_w, new_h = resize_image(image1)  # Resize uploaded image

    face_detector.setInputSize([image1_resized.shape[1], image1_resized.shape[0]])
    faces1 = face_detector.infer(image1_resized)

    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return [], image1  # Return original image

    # Visualize faces detected in the uploaded image
    image1_with_faces, face_bboxes = visualize_faces(image1_resized, faces1)

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)
        if image2 is not None:
            image2_resized, _, _ = resize_image(image2)  # Resize comparison image
            face_detector.setInputSize([image2_resized.shape[1], image2_resized.shape[0]])
            faces2 = face_detector.infer(image2_resized)

            if faces2.shape[0] > 0:
                result = face_recognizer.match(image1_resized, faces1[0][:-1], image2_resized, faces2[0][:-1])
                results.append((filename, result[0], result[1]))

    return results, image1_with_faces  # Return image with detected faces

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

        results, image_with_faces = find_similar_faces(uploaded_image, folder_path)

        # Display image with visualized faces only
        st.image(image_with_faces, channels="BGR", caption="Detected Faces", use_column_width=True)

        if results:
            # Find the result with the highest score
            best_match = max(results, key=lambda x: x[1])
            st.subheader("Best Match Found:")
            st.write(f"File: {best_match[0]}, Similarity Score: {best_match[1]:.2f}")
            student_info = read_student_info(best_match[0], folder_path)
            st.write(f"Student Information: {student_info}")
        else:
            st.warning("No similar faces found.")

if __name__ == "__main__":
    run_app5()
