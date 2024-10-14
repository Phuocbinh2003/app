import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
from Face_Verification.yunet import YuNet
from Face_Verification.sface import SFace

# Thiết lập các backend và target hợp lệ cho OpenCV DNN
backend_target_pairs = [
    [cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_TARGET_CPU],
]

backend_id = backend_target_pairs[0][0]
target_id = backend_target_pairs[0][1]

# Khởi tạo mô hình YuNet cho phát hiện khuôn mặt
face_detector = YuNet(
    modelPath="Face_Verification/face_detection_yunet_2023mar.onnx",
    inputSize=[320, 320],
    confThreshold=0.5,
    nmsThreshold=0.3,
    topK=5000,
    backendId=backend_id,
    targetId=target_id
)

# Khởi tạo mô hình SFace cho nhận diện khuôn mặt
face_recognizer = SFace(
    modelPath="Face_Verification/face_recognition_sface_2021dec.onnx",
    disType=0,  # cosine
    backendId=backend_id,
    targetId=target_id
)

def visualize_matches(img1, faces1, img2, faces2, matches, scores, target_size=[512, 512]):
    """Hiển thị kết quả so khớp khuôn mặt giữa hai ảnh."""
    out1 = img1.copy()
    out2 = img2.copy()
    matched_box_color = (0, 255, 0)  # Màu cho khung vuông trùng khớp
    mismatched_box_color = (0, 0, 255)  # Màu cho khung vuông không trùng khớp

    # Resize và tạo khung cho ảnh 1
    padded_out1 = resize_and_pad(out1, target_size)
    bbox1 = faces1[0][:4] * (target_size[0] / out1.shape[0])
    draw_bounding_box(padded_out1, bbox1, matched_box_color)

    # Resize và tạo khung cho ảnh 2
    padded_out2 = resize_and_pad(out2, target_size)
    assert faces2.shape[0] == len(matches), "Số lượng khuôn mặt trong ảnh 2 phải khớp với số lượng kết quả so khớp."
    for index, match in enumerate(matches):
        bbox2 = faces2[index][:4] * (target_size[0] / out2.shape[0])
        box_color = matched_box_color if match else mismatched_box_color
        draw_bounding_box(padded_out2, bbox2, box_color, scores[index])

    return np.concatenate([padded_out1, padded_out2], axis=1)

def draw_bounding_box(image, bbox, color, score=None):
    """Vẽ khung vuông quanh khuôn mặt trong ảnh."""
    x, y, w, h = bbox.astype(np.int32)
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    if score is not None:
        text_color = color
        cv2.putText(image, "{:.2f}".format(score), (x, y - 5), cv2.FONT_HERSHEY_DUPLEX, 0.4, text_color)

def resize_and_pad(image, target_size):
    """Resize và tạo khung cho ảnh để phù hợp với kích thước mục tiêu."""
    padded_image = np.zeros((target_size[0], target_size[1], 3), dtype=np.uint8)
    h, w, _ = image.shape
    ratio = min(target_size[0] / h, target_size[1] / w)
    new_h = int(h * ratio)
    new_w = int(w * ratio)
    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    top = (target_size[0] - new_h) // 2
    bottom = top + new_h
    left = (target_size[1] - new_w) // 2
    right = left + new_w
    padded_image[top:bottom, left:right] = resized_image
    return padded_image

def calculate_similarity(features1, features2):
    """Tính toán điểm tương đồng giữa hai vector đặc trưng từ SFace."""
    if features1 is None or features2 is None:
        return None  # Trả về None nếu không có đặc trưng nào được trích xuất
    distance = np.linalg.norm(features1 - features2)
    similarity = 1 / (1 + distance)
    return similarity

def extract_face(image):
    """Tách khuôn mặt từ ảnh và trả về ảnh khuôn mặt đã cắt ra."""
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    resized_image = resize_image(image_bgr)

    face_detector.setInputSize([resized_image.shape[1], resized_image.shape[0]])
    faces = face_detector.infer(resized_image)

    if faces.shape[0] == 0:
        st.warning("Không phát hiện khuôn mặt nào trong ảnh.")
        return None

    bbox = faces[0][:4].astype(np.int32)
    x, y, w, h = bbox
    face_image = image[y:y + h, x:x + w]
    return face_image

def find_similar_faces(uploaded_image, folder_path):
    """Tìm khuôn mặt tương tự trong thư mục dựa trên ảnh đã tải lên."""
    results = []
    image1 = Image.open(uploaded_image).convert("RGB")
    image1_np = np.array(image1)
    image1_bgr = cv2.cvtColor(image1_np, cv2.COLOR_RGB2BGR)

    image1_resized = resize_image(image1_bgr)
    face_detector.setInputSize([image1_resized.shape[1], image1_resized.shape[0]])
    faces1 = face_detector.infer(image1_resized)

    if faces1.shape[0] == 0:
        st.warning("Không phát hiện khuôn mặt trong ảnh đã tải lên.")
        return [], image1

    image1_with_faces, face_bboxes = visualize_faces(image1_resized, faces1)
    st.image(cv2.cvtColor(image1_with_faces, cv2.COLOR_BGR2RGB), caption="Hình ảnh đã xử lý với khuôn mặt được phát hiện", use_column_width=True)

    best_match_filename = None
    best_score = 0.0

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        image2 = cv2.imread(img_path)
        if image2 is not None:
            image2_resized = resize_image(image2)
            face_detector.setInputSize([image2_resized.shape[1], image2_resized.shape[0]])
            faces2 = face_detector.infer(image2_resized)

            if faces2.shape[0] > 0:
                result = face_recognizer.match(image1_resized, faces1[0][:-1], image2_resized, faces2[0][:-1])
                score = result[1]

                if score > best_score:
                    best_score = score
                    best_match_filename = filename

    return best_match_filename, best_score, image1_with_faces

def visualize_faces(image, results, box_color=(0, 255, 0), text_color=(0, 0, 255), fps=None):
    """Hiển thị khuôn mặt phát hiện trong ảnh."""
    output = image.copy()
    landmark_color = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 255), (0, 255, 255)]

    if fps is not None:
        cv2.putText(output, 'FPS: {:.2f}'.format(fps), (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color)

    for det in results:
        bbox = det[0:4].astype(np.int32)
        draw_bounding_box(output, bbox, box_color)
        landmarks = det[4:14].astype(np.int32).reshape((5, 2))
        for idx, landmark in enumerate(landmarks):
            cv2.circle(output, landmark, 2, landmark_color[idx], 2)

    return output

def resize_image(image, target_size=320):
    """Resize ảnh để phù hợp với kích thước mục tiêu và giữ tỷ lệ khung hình."""
    h, w, _ = image.shape
    if w > h:
        new_w = target_size
        new_h = int(h * (target_size / w))
    else:
        new_h = target_size
        new_w = int(w * (target_size / h))

    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    return resized_image

def read_student_info(filename, folder_path):
    """Đọc thông tin sinh viên từ tệp văn bản."""
    txt_file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.txt")
    with open(txt_file_path, "r", encoding="utf-8") as txt_file:
        content = txt_file.read()
    return content

def show_student_info(student_image, folder_path):
    """Hiển thị thông tin sinh viên dựa trên ảnh đã tải lên."""
    filename = os.path.basename(student_image)
    student_info = read_student_info(filename, folder_path)

    st.header("Thông tin sinh viên:")
    st.write(student_info)

def run_app5():
    """Phần 1: Tìm khuôn mặt giống nhất trong thư mục."""
    
    st.title("Face Recognition - Find Similar Faces in a Folder")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        folder_path = "Face_Verification/image"  # Đường dẫn thư mục
        if os.path.isdir(folder_path):
            st.write(f"Finding similar faces in the folder: {folder_path}")
            best_match_filename, best_score, processed_image = find_similar_faces(uploaded_image, folder_path)

            # Hiển thị hình ảnh đã xử lý với khuôn mặt được phát hiện
           # st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), caption="Processed Image with Detected Faces", use_column_width=True)

            if best_match_filename is not None:
                st.write(f"### Best Match Found:")
                st.write(f"- {best_match_filename} | Score: {best_score:.2f}")

                # Hiển thị thông tin của học sinh
                student_info = read_student_info(best_match_filename, folder_path)
                st.write(f"**Thông tin học sinh:** {student_info}")
            else:
                st.warning("No matching faces found.")
        else:
            st.error(f"Folder '{folder_path}' does not exist.")

    """Phần 2: So sánh ảnh chân dung và ảnh thẻ."""
    st.header("Compare Portrait and ID Photo")
    uploaded_image1 = st.file_uploader("Upload Portrait Image...", type=["jpg", "jpeg", "png"], key="portrait")
    uploaded_image2 = st.file_uploader("Upload ID Image...", type=["jpg", "jpeg", "png"], key="id")

    if uploaded_image1 and uploaded_image2:
        image1 = Image.open(uploaded_image1).convert("RGB")
        image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)

        image2 = Image.open(uploaded_image2).convert("RGB")
        image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)

        # Resize images
        image1_resize = resize_image(image1)
        image2_resize = resize_image(image2)

        # Compare faces and get the score
        score = compare_faces(image1_resize, image2_resize)

        if score is not None:
            st.success(f"Similarity Score: {score:.2f}")

            # Visualize the matches on the images
            faces1 = face_detector.infer(image1)
            faces2 = face_detector.infer(image2)
            
            st.write(f"faces1: {faces1}")
            st.write(f"faces2: {faces2}")


            # Visualize matches only if faces are detected
            if faces1.shape[0] > 0 and faces2.shape[0] > 0:
                matches = [1]  # Assuming a match for visualization, adjust logic as needed
                scores = [score]  # Using the score for visualization
                matched_image = visualize_matches(image1_resize, faces1, image2_resize, faces2, matches, scores)

                # Display the matched image
                st.image(cv2.cvtColor(matched_image, cv2.COLOR_BGR2RGB), caption="Matched Images", use_column_width=True)
        else:
            st.warning("Could not compare the images, no faces detected.")

if __name__ == "__main__":
    run_app5()
