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

def visualize_matches(img1, faces1, img2, faces2, matches, scores, target_size=[512, 512]):
    """Visualizes matches between two images."""
    out1, out2 = img1.copy(), img2.copy()
    matched_box_color, mismatched_box_color = (0, 255, 0), (0, 0, 255)

    # Resize and pad the first image
    padded_out1 = resize_and_pad(out1, target_size)
    draw_bounding_boxes(padded_out1, faces1, matches, matched_box_color, mismatched_box_color)

    # Resize and pad the second image
    padded_out2 = resize_and_pad(out2, target_size)
    draw_bounding_boxes(padded_out2, faces2, matches, matched_box_color, mismatched_box_color, scores)

    return np.concatenate([padded_out1, padded_out2], axis=1)

def resize_and_pad(image, target_size):
    """Resizes and pads an image to the target size."""
    padded_out = np.zeros((target_size[0], target_size[1], 3)).astype(np.uint8)
    h, w, _ = image.shape
    ratio = min(target_size[0] / h, target_size[1] / w)
    new_h, new_w = int(h * ratio), int(w * ratio)
    resized_out = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    top, bottom = (target_size[0] - new_h) // 2, (target_size[0] - new_h) // 2 + new_h
    left, right = (target_size[1] - new_w) // 2, (target_size[1] - new_w) // 2 + new_w
    padded_out[top:bottom, left:right] = resized_out
    return padded_out

def draw_bounding_boxes(image, faces, matches, matched_box_color, mismatched_box_color, scores=None):
    """Draws bounding boxes on the given image."""
    for index, match in enumerate(matches):
        bbox = faces[index][:4].astype(np.int32)
        box_color = matched_box_color if match else mismatched_box_color
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), box_color, 2)

        if scores is not None:
            score = scores[index]
            text_color = matched_box_color if match else mismatched_box_color
            cv2.putText(image, "{:.2f}".format(score), (bbox[0], bbox[1] - 5), cv2.FONT_HERSHEY_DUPLEX, 0.4, text_color)

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
    return resized_image

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
    image1 = resize_image(image1)  # Use resize_image for the uploaded image

    face_detector.setInputSize([image1.shape[1], image1.shape[0]])
    faces1 = face_detector.infer(image1)

    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return []

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)
        if image2 is not None:
            image2 = resize_image(image2)  # Use resize_image for the comparison images
            face_detector.setInputSize([image2.shape[1], image2.shape[0]])
            faces2 = face_detector.infer(image2)

            if faces2.shape[0] > 0:
                result = face_recognizer.match(image1, faces1[0][:-1], image2, faces2[0][:-1])
                results.append((filename, result[0], result[1]))

    return results

def compare_faces(image1, image2):
    """Compares two images and returns a similarity score."""
    faces1 = face_detector.infer(image1)
    faces2 = face_detector.infer(image2)

    if faces1.shape[0] == 0 or faces2.shape[0] == 0:
        return 0.0  # No faces found, return score of 0

    result = face_recognizer.match(image1, faces1[0][:-1], image2, faces2[0][:-1])
    return result[0]  # Return similarity score

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
            st.subheader("Similar Faces Found:")
            for filename, score, _ in results:
                st.write(f"File: {filename}, Similarity Score: {score:.2f}")
                student_info = read_student_info(filename, folder_path)
                st.write(f"Student Information: {student_info}")
        else:
            st.warning("No similar faces found.")

if __name__ == "__main__":
    run_app5()
