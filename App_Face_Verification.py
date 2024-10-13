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

def visualize_faces(image, results, box_color=(0, 255, 0), text_color=(0, 0, 255)):
    output = image.copy()

    if results:
        best_result = max(results, key=lambda x: x[-1])  # Get the result with the highest score
        bbox = best_result[0:4].astype(np.int32)
        cv2.rectangle(output, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), box_color, 2)

        conf = best_result[-1]
        cv2.putText(output, '{:.4f}'.format(conf), (bbox[0], bbox[1] + 12), cv2.FONT_HERSHEY_DUPLEX, 0.5, text_color)

        # Draw landmarks for the best result
        landmarks = best_result[4:14].astype(np.int32).reshape((5, 2))
        for idx, landmark in enumerate(landmarks):
            cv2.circle(output, landmark, 2, box_color, 2)

    return output

def find_similar_faces(uploaded_image, folder_path):
    results = []
    # Convert uploaded image to NumPy array
    image1 = Image.open(uploaded_image).convert("RGB")
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)

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
        if image2 is not None:
            # Resize image before processing
            image2 = resize_image(image2)
            face_detector.setInputSize([image2.shape[1], image2.shape[0]])
            faces2 = face_detector.infer(image2)

            if faces2.shape[0] > 0:
                result = face_recognizer.match(image1, faces1[0][:-1], image2, faces2[0][:-1])
                results.append((filename, result[0], result[1]))

    # Visualize faces on the uploaded image
    visualized_image = visualize_faces(image1, faces1)
    return results, visualized_image

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
        st.image(uploaded_image, caption='Uploaded Image', use_column_width=True)

        results, visualized_image = find_similar_faces(uploaded_image, folder_path)
        if results:
            st.subheader("Matched Faces:")
            best_match = max(results, key=lambda x: x[1])  # Get the best match based on score
            filename, score, _ = best_match
            st.write(f"Found similar face in {filename} with score: {score:.2f}")
            student_info = read_student_info(filename, folder_path)
            st.write(student_info)

            # Display the visualized image with bounding box
            st.image(visualized_image, caption='Visualized Detected Faces', use_column_width=True)

        else:
            st.warning("No similar faces found.")

    # Part 2: Compare portrait with ID photo
    st.header("Compare Portrait Image with ID Image")
    portrait_image = st.file_uploader("Upload Portrait Image...", type=["jpg", "jpeg", "png"], key="portrait")
    id_image = st.file_uploader("Upload ID Image...", type=["jpg", "jpeg", "png"], key="id")

    if portrait_image and id_image:
        portrait = Image.open(portrait_image).convert("RGB")
        id_img = Image.open(id_image).convert("RGB")
        
        # Convert to BGR
        portrait = cv2.cvtColor(np.array(portrait), cv2.COLOR_RGB2BGR)
        id_img = cv2.cvtColor(np.array(id_img), cv2.COLOR_RGB2BGR)

        # Resize images before processing
        portrait = resize_image(portrait)
        id_img = resize_image(id_img)

        similarity_score = compare_faces(portrait, id_img)
        st.image(portrait, caption='Portrait Image', use_column_width=True)
        st.image(id_img, caption='ID Image', use_column_width=True)
        st.write(f"Similarity Score: {similarity_score:.2f}")

        if similarity_score > 0.5:  # Threshold for considering them as the same person
            st.success("The images match!")
        else:
            st.error("The images do not match.")

if __name__ == "__main__":
    run_app5()
