import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
from Face_Verification.yunet import YuNet
from Face_Verification.sface import SFace

# Backend and target setup
backend_id = cv2.dnn.DNN_BACKEND_OPENCV
target_id = cv2.dnn.DNN_TARGET_CPU

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

def visualize_matches(img1, faces1, img2, faces2, matches, scores, target_size=[512, 512]):
    out1 = img1.copy()
    out2 = img2.copy()
    matched_box_color = (0, 255, 0)  # Green for matched
    mismatched_box_color = (0, 0, 255)  # Red for mismatched

    # Process image 1
    padded_out1 = process_image_for_visualization(out1, target_size)
    draw_face_boxes(padded_out1, faces1, matched_box_color)

    # Process image 2
    padded_out2 = process_image_for_visualization(out2, target_size)
    draw_face_boxes_with_scores(padded_out2, faces2, matches, scores, matched_box_color, mismatched_box_color)

    return np.concatenate([padded_out1, padded_out2], axis=1)

def process_image_for_visualization(image, target_size):
    """Resize image and pad to target size for visualization."""
    padded_image = np.zeros((target_size[0], target_size[1], 3), dtype=np.uint8)
    h, w, _ = image.shape
    ratio = min(target_size[0] / h, target_size[1] / w)
    new_h = int(h * ratio)
    new_w = int(w * ratio)
    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    top, bottom = (target_size[0] - new_h) // 2, (target_size[0] - new_h + 1) // 2
    left, right = (target_size[1] - new_w) // 2, (target_size[1] - new_w + 1) // 2
    padded_image[top:top + new_h, left:left + new_w] = resized_image
    return padded_image

def draw_face_boxes(image, faces, color):
    """Draw bounding boxes around detected faces."""
    for face in faces:
        bbox = face[:4].astype(np.int32)
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 2)

def draw_face_boxes_with_scores(image, faces, matches, scores, matched_color, mismatched_color):
    """Draw bounding boxes with scores around detected faces."""
    for index, match in enumerate(matches):
        bbox = faces[index][:4].astype(np.int32)
        color = matched_color if match else mismatched_color
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), color, 2)
        cv2.putText(image, f"{scores[index]:.2f}", (bbox[0], bbox[1] - 5), cv2.FONT_HERSHEY_DUPLEX, 0.4, color)

def find_similar_faces(uploaded_image, folder_path):
    """Finds similar faces in a folder based on the uploaded image."""
    # Convert uploaded image to BGR
    image1 = Image.open(uploaded_image).convert("RGB")
    image1_np = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    image1_resized = resize_image(image1_np)

    # Detect faces
    faces1 = face_detector.infer(image1_resized)
    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return None, 0.0, image1_np  # No faces detected

    # Process comparison
    best_match_filename, best_score = None, 0.0
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)
        if image2 is not None:
            image2_resized = resize_image(image2)
            faces2 = face_detector.infer(image2_resized)
            if faces2.shape[0] > 0:
                score = face_recognizer.match(image1_resized, faces1[0][:-1], image2_resized, faces2[0][:-1])[1]
                if score > best_score:
                    best_score = score
                    best_match_filename = filename

    return best_match_filename, best_score, image1_np

def resize_image(image, target_size=320):
    """Resize image while maintaining aspect ratio."""
    h, w, _ = image.shape
    if w > h:
        new_w = target_size
        new_h = int(h * (target_size / w))
    else:
        new_h = target_size
        new_w = int(w * (target_size / h))
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

def run_app5():
    """Run Streamlit Face Recognition app."""
    st.title("Face Recognition - Find Similar Faces in a Folder")
    
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        folder_path = "Face_Verification/image"  # Define folder path
        if os.path.isdir(folder_path):
            st.write(f"Finding similar faces in the folder: {folder_path}")
            best_match_filename, best_score, processed_image = find_similar_faces(uploaded_image, folder_path)
            st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), caption="Processed Image with Detected Faces", use_column_width=True)

            if best_match_filename:
                st.write(f"### Best Match Found: {best_match_filename} | Score: {best_score:.2f}")
                student_info = read_student_info(best_match_filename, folder_path)
                st.write(f"**Student Information:** {student_info}")
            else:
                st.warning("No matching faces found.")
        else:
            st.error(f"Folder '{folder_path}' does not exist.")

    st.header("Compare Portrait and ID Photo")
    uploaded_image1 = st.file_uploader("Upload Portrait Image...", type=["jpg", "jpeg", "png"], key="portrait")
    uploaded_image2 = st.file_uploader("Upload ID Image...", type=["jpg", "jpeg", "png"], key="id")

    if uploaded_image1 and uploaded_image2:
        image1 = Image.open(uploaded_image1).convert("RGB")
        image1_bgr = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)

        image2 = Image.open(uploaded_image2).convert("RGB")
        image2_bgr = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)

        # Resize images for comparison
        image1_resized = resize_image(image1_bgr)
        image2_resized = resize_image(image2_bgr)

        # Compare faces
        score = compare_faces(image1_resized, image2_resized)
        if score is not None:
            st.success(f"Similarity Score: {score:.2f}")
        else:
            st.warning("Could not compare the faces.")

# Run the Streamlit application
if __name__ == "__main__":
    run_app5()
