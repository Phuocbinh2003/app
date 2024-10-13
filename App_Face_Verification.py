import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
from Face_Verification.yunet import YuNet
from Face_Verification.sface import SFace

# Valid combinations of backends and target
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

def visualize_matches(img1, faces1, img2, faces2, matches, scores, target_size=[512, 512]):
    out1 = img1.copy()
    out2 = img2.copy()
    matched_box_color = (0, 255, 0)  # BGR
    mismatched_box_color = (0, 0, 255)  # BGR

    # Resize to target size for image 1
    padded_out1 = np.zeros((target_size[0], target_size[1], 3)).astype(np.uint8)
    h1, w1, _ = out1.shape
    ratio1 = min(target_size[0] / out1.shape[0], target_size[1] / out1.shape[1])
    new_h1 = int(h1 * ratio1)
    new_w1 = int(w1 * ratio1)
    resized_out1 = cv2.resize(out1, (new_w1, new_h1), interpolation=cv2.INTER_LINEAR)
    top = max(0, target_size[0] - new_h1) // 2
    bottom = top + new_h1
    left = max(0, target_size[1] - new_w1) // 2
    right = left + new_w1
    padded_out1[top:bottom, left:right] = resized_out1

    # Draw bbox for image 1
    bbox1 = faces1[0][:4] * ratio1
    x, y, w, h = bbox1.astype(np.int32)
    cv2.rectangle(padded_out1, (x + left, y + top), (x + left + w, y + top + h), matched_box_color, 2)

    # Resize to target size for image 2
    padded_out2 = np.zeros((target_size[0], target_size[1], 3)).astype(np.uint8)
    h2, w2, _ = out2.shape
    ratio2 = min(target_size[0] / out2.shape[0], target_size[1] / out2.shape[1])
    new_h2 = int(h2 * ratio2)
    new_w2 = int(w2 * ratio2)
    resized_out2 = cv2.resize(out2, (new_w2, new_h2), interpolation=cv2.INTER_LINEAR)
    top = max(0, target_size[0] - new_h2) // 2
    bottom = top + new_h2
    left = max(0, target_size[1] - new_w2) // 2
    right = left + new_w2
    padded_out2[top:bottom, left:right] = resized_out2

    # Draw bbox for image 2
    assert faces2.shape[0] == len(matches), "number of faces2 needs to match matches"
    assert len(matches) == len(scores), "number of matches needs to match number of scores"
    for index, match in enumerate(matches):
        bbox2 = faces2[index][:4] * ratio2
        x, y, w, h = bbox2.astype(np.int32)
        box_color = matched_box_color if match else mismatched_box_color
        cv2.rectangle(padded_out2, (x + left, y + top), (x + left + w, y + top + h), box_color, 2)

        score = scores[index]
        text_color = matched_box_color if match else mismatched_box_color
        cv2.putText(padded_out2, "{:.2f}".format(score), (x + left, y + top - 5), cv2.FONT_HERSHEY_DUPLEX, 0.4, text_color)

    return np.concatenate([padded_out1, padded_out2], axis=1)


def find_similar_faces(uploaded_image, folder_path):
    """Finds similar faces in a folder based on the uploaded image."""
    results = []
    
    # Open the uploaded image and convert to RGB
    image1 = Image.open(uploaded_image).convert("RGB")
    image1_np = np.array(image1)  # Convert to NumPy array
    image1_bgr = cv2.cvtColor(image1_np, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV

    # Resize the uploaded image for detection
    face_detector.setInputSize([image1_bgr.shape[1], image1_bgr.shape[0]])
    
    # Detect faces in the uploaded image
    faces1 = face_detector.infer(image1_bgr)

    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return [], image1_bgr  # Return original image if no faces detected

    # Visualize faces in the uploaded image
    image1_with_faces = visualize_faces(image1_bgr, faces1)

    # Now compare this image with others in the folder
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)
        if image2 is not None:
            face_detector.setInputSize([image2.shape[1], image2.shape[0]])
            faces2 = face_detector.infer(image2)

            if faces2.shape[0] > 0:
                result = face_recognizer.match(image1_bgr, faces1[0][:-1], image2, faces2[0][:-1])
                results.append((filename, result[0], result[1]))

    return results, image1_with_faces  # Return the image with faces drawn


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
    h, w, _ = image.shape
    # Check which dimension is larger
    if w > h:
        new_w = target_size
        new_h = int(h * (target_size / w))  # Calculate height based on width
    else:
        new_h = target_size
        new_w = int(w * (target_size / h))  # Calculate width based on height

    # Resize image while keeping aspect ratio
    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    return resized_image

def read_student_info(filename, folder_path):
    txt_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.txt")
    with open(txt_file_path, "r", encoding="utf-8") as txt_file:
        student_info = txt_file.read().strip()
    return student_info

def run_app5():
    st.title("Face Verification Application")

    uploaded_image = st.file_uploader("Upload an image for verification", type=["jpg", "jpeg", "png"])
    folder_path = "Face_Verification/image"  # Update with your folder path

    if uploaded_image is not None:
        results, processed_image = find_similar_faces(uploaded_image, folder_path)

        # Show the image with visualized faces
        st.image(processed_image, caption="Image with Detected Faces", use_column_width=True)

        if results:
            for filename, score, is_match in results:
                st.write(f"Compared with: {filename}, Match Score: {score:.2f}")
                if is_match:
                    student_info = read_student_info(filename, folder_path)
                    st.write(f"Student Information: {student_info}")

        else:
            st.warning("No matches found.")

if __name__ == "__main__":
    run_app5()
