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
    ratio1 = min(target_size[0] / h1, target_size[1] / w1)
    new_h1 = int(h1 * ratio1)
    new_w1 = int(w1 * ratio1)
    resized_out1 = cv2.resize(out1, (new_w1, new_h1), interpolation=cv2.INTER_LINEAR)
    top = (target_size[0] - new_h1) // 2
    bottom = top + new_h1
    left = (target_size[1] - new_w1) // 2
    right = left + new_w1
    padded_out1[top:bottom, left:right] = resized_out1

    # Draw bbox for image 1
    bbox1 = faces1[0][:4] * ratio1
    x, y, w, h = bbox1.astype(np.int32)
    cv2.rectangle(padded_out1, (x + left, y + top), (x + left + w, y + top + h), matched_box_color, 2)

    # Resize to target size for image 2
    padded_out2 = np.zeros((target_size[0], target_size[1], 3)).astype(np.uint8)
    h2, w2, _ = out2.shape
    ratio2 = min(target_size[0] / h2, target_size[1] / w2)
    new_h2 = int(h2 * ratio2)
    new_w2 = int(w2 * ratio2)
    resized_out2 = cv2.resize(out2, (new_w2, new_h2), interpolation=cv2.INTER_LINEAR)
    top = (target_size[0] - new_h2) // 2
    bottom = top + new_h2
    left = (target_size[1] - new_w2) // 2
    right = left + new_w2
    padded_out2[top:bottom, left:right] = resized_out2

    # Draw bbox for image 2
    assert faces2.shape[0] == len(matches), "Number of faces2 needs to match matches"
    assert len(matches) == len(scores), "Number of matches needs to match number of scores"
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
    results = []
    # Convert uploaded image to NumPy array
    image1 = Image.open(uploaded_image).convert("RGB")  # Convert to RGB
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)  # Convert to BGR

    # Resize image before processing
    image1 = resize_image(image1)

    face_detector.setInputSize([image1.shape[1], image1.shape[0]])
    faces1 = face_detector.infer(image1)

    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return []

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)
        if image2 is not None:  # Check if image was read successfully
            # Resize image before processing
            image2 = resize_image(image2)
            face_detector.setInputSize([image2.shape[1], image2.shape[0]])
            faces2 = face_detector.infer(image2)

            if faces2.shape[0] > 0:
                result = face_recognizer.match(image1, faces1[0][:-1], image2, faces2[0][:-1])
                results.append((filename, result[0], result[1]))

    return results

def visualize_faces(image, results, box_color=(0, 255, 0), text_color=(0, 0, 255), fps=None):
    output = image.copy()
    landmark_color = [
        (255, 0, 0),   # right eye
        (0, 0, 255),   # left eye
        (0, 255, 0),   # nose tip
        (255, 0, 255), # right mouth corner
        (0, 255, 255)  # left mouth corner
    ]

    if fps is not None:
        cv2.putText(output, 'FPS: {:.2f}'.format(fps), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color)

    bboxes = []  # List to store bounding boxes
    for det in results:
        bbox = det[0:4].astype(np.int32)
        cv2.rectangle(output, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), box_color, 2)

        # Save the bounding box position
        bboxes.append(bbox)

        conf = det[-1]
        cv2.putText(output, '{:.4f}'.format(conf), (bbox[0], bbox[1]+12), cv2.FONT_HERSHEY_DUPLEX, 0.5, text_color)

        landmarks = det[4:14].astype(np.int32).reshape((5, 2))
        for idx, landmark in enumerate(landmarks):
            cv2.circle(output, landmark, 2, landmark_color[idx], 2)

    return output, bboxes  # Return both the output and bboxes

def resize_image(image, target_size=(320, 239)):
    # Resize the image to the specified target size
    resized_image = cv2.resize(image, target_size, interpolation=cv2.INTER_LINEAR)
    return resized_image

def read_student_info(filename, folder_path):
    txt_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.txt")
    if os.path.exists(txt_file_path):
        with open(txt_file_path, "r") as f:
            return f.read()
    else:
        return "No student information found."

def compare_faces(image1, image2):
    # Detect faces in both images
    faces1 = face_detector.infer(image1)
    faces2 = face_detector.infer(image2)

    if faces1.shape[0] == 0 or faces2.shape[0] == 0:
        return 0.0  # No faces found, return score of 0

    # Compare the first detected face from each image
    result = face_recognizer.match(image1, faces1[0][:-1], image2, faces2[0][:-1])
    return result[0]  # Return similarity score

def run_app5():
    st.title("Face Recognition App")

    # Part 1: Find student information from image
    st.header("Find Student Information from Image")
    uploaded_image = st.file_uploader("Upload Image...", type=["jpg", "jpeg", "png"], key="image")

    if uploaded_image is not None:
        folder_path = "Face_Verification/image"  # Update with your folder path

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

        # Compare uploaded images
        if uploaded_image is not None:
            score = compare_faces(image1, image2)

            st.image(image2, channels="BGR", caption="Comparison Image", use_column_width=True)
            st.write(f"Similarity Score: {score:.4f}")

            # Display images side by side with bounding boxes
            vis_image = visualize_matches(image1, faces1, image2, faces2, [score > 0.5], [score])
            st.image(vis_image, channels="BGR", caption="Comparison Result", use_column_width=True)
        else:
            st.warning("Please upload the first image for comparison.")

if __name__ == "__main__":
    run_app5()
