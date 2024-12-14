import streamlit as st
import cv2
import numpy as np
import os
from PIL import Image
from Face_Verification.yunet import YuNet
from Face_Verification.sface import SFace

# Valid combinations of backends and targe
backend_target_pairs = [
    [cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_TARGET_CPU],
]

backend_id = backend_target_pairs[0][0]
target_id = backend_target_pairs[0][1]

# Instantiate YuNe
face_detector = YuNet(
    modelPath="Face_Verification/face_detection_yunet_2023mar.onnx",
    inputSize=[1024, 1024],
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

def calculate_similarity(faces1, faces2):
    """
    Tính toán điểm tương đồng giữa hai danh sách các khuôn mặt.

    Args:
        faces1: Danh sách các đặc trưng khuôn mặt từ hình ảnh đầu tiên.
        faces2: Danh sách các đặc trưng khuôn mặt từ hình ảnh thứ hai.

    Returns:
        Điểm tương đồng giữa hai hình ảnh (0 đến 1), hoặc None nếu không có khuôn mặt nào.
    """
    if len(faces1) == 0 or len(faces2) == 0:
        return None  # Trả về None nếu không có khuôn mặt nào được phát hiện

    # Giả sử faces chứa các vector đặc trưng khuôn mặt
    # Tính toán Euclidean Distance
    # Chỉ cần so sánh khuôn mặt đầu tiên của mỗi danh sách
    distance = np.linalg.norm(faces1[0] - faces2[0])  # Tính khoảng cách Euclidean
    similarity = 1 / (1 + distance)  # Chuyển đổi khoảng cách thành điểm tương đồng

    return similarity

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

def extract_face(image):
    """Tách khuôn mặt từ ảnh sử dụng mô hình YuNet và trả về ảnh khuôn mặt đã cắt ra."""
    # Kích thước mà bạn muốn resize ảnh về trước khi đưa vào mô hình
    desired_size = (250, 250)

    # Resize ảnh và lưu tỷ lệ thay đổi
    h_orig, w_orig = image.shape[:2]
    resized_image = cv2.resize(image, desired_size)
    scale_x = w_orig / desired_size[0]
    scale_y = h_orig / desired_size[1]

    # Cài đặt kích thước đầu vào cho mô hình
    face_detector.setInputSize([resized_image.shape[1], resized_image.shape[0]])

    # Phát hiện khuôn mặt
    faces = face_detector.infer(resized_image)

    if faces.shape[0] == 0:
        st.warning("Không phát hiện khuôn mặt nào trong ảnh.")
        return None  # Trả về None nếu không phát hiện khuôn mặt

    # Lấy bounding box của khuôn mặt đầu tiên
    bbox = faces[0][:4].astype(np.int32)

    # Scale lại tọa độ bounding box để khớp với ảnh gốc
    x, y, w, h = bbox
    x = int(x * scale_x)
    y = int(y * scale_y)
    w = int(w * scale_x)
    h = int(h * scale_y)

    # Đảm bảo bounding box không vượt quá giới hạn ảnh gốc
    x = max(0, x)
    y = max(0, y)
    w = min(w_orig - x, w)
    h = min(h_orig - y, h)

    # Cắt khuôn mặt từ ảnh gốc
    face_image = image[y:y + h, x:x + w]

    return face_image  # Trả về ảnh khuôn mặt đã cắt ra
def extract_face_the_sv(image):
    """Tách khuôn mặt từ ảnh sử dụng mô hình YuNet và trả về ảnh khuôn mặt đã cắt ra."""
    # Chuyển đổi ảnh sang định dạng BGR cho OpenCV
    # image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Resize ảnh để phù hợp với kích thước đầu vào của mô hình
    # resized_image = resize_image(image)

    # Cài đặt kích thước đầu vào cho mô hình
    face_detector.setInputSize([image.shape[1], image.shape[0]])

    # Phát hiện khuôn mặt
    faces = face_detector.infer(image)

    if faces.shape[0] == 0:
        st.warning("Không phát hiện khuôn mặt nào trong ảnh.")
        return None  # Trả về None nếu không phát hiện khuôn mặt

    # Lấy bounding box của khuôn mặt đầu tiên
    bbox = faces[0][:4].astype(np.int32)

    # Cắt khuôn mặt từ ảnh gốc
    x, y, w, h = bbox
    face_image = image[y:y + h, x:x + w]

    return face_image  # Trả về ảnh khuôn mặt đã cắt ra

def find_similar_faces(uploaded_image, folder_path):
    """Finds the most similar face in a folder to the uploaded image."""
    results = []

    # Step 1: Open and preprocess the uploaded image
    try:
        image1 = Image.open(uploaded_image).convert("RGB")  # Open and convert to RGB
        image1_np = np.array(image1)  # Convert to NumPy array
        image1_bgr = cv2.cvtColor(image1_np, cv2.COLOR_RGB2BGR)  # Convert to BGR for OpenCV
    except Exception as e:
        st.error(f"Error processing uploaded image: {e}")
        return None, None, None

    # Step 2: Detect faces in the uploaded image
    face_detector.setInputSize([image1_bgr.shape[1], image1_bgr.shape[0]])
    faces1 = face_detector.infer(image1_bgr)

    if faces1.shape[0] == 0:
        st.warning("No face detected in the uploaded image.")
        return None, None, image1  # Return original image if no faces detected

    # Visualize detected faces on the uploaded image
    image1_with_faces, face_bboxes = visualize_faces(image1_bgr, faces1)
    st.image(cv2.cvtColor(image1_with_faces, cv2.COLOR_BGR2RGB), caption="Uploaded Image with Detected Faces", use_column_width=True)

    # Step 3: Compare with images in the folder
    best_match_filename = None
    best_score = 0.0

    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        try:
            # Read and preprocess each image from the folder
            image2 = cv2.imread(img_path)
            if image2 is None:
                continue

            image2_resized = resize_image(image2)
            face_detector.setInputSize([image2_resized.shape[1], image2_resized.shape[0]])
            faces2 = face_detector.infer(image2_resized)

            if faces2.shape[0] > 0:
                # Match the uploaded face with the detected face in the current folder image
                match_result = face_recognizer.match(image1_bgr, faces1[0][:-1], image2_resized, faces2[0][:-1])
                score = match_result[1]  # Similarity score

                # Update best match if the score is higher
                if score > best_score:
                    best_score = score
                    best_match_filename = filename
        except Exception as e:
            st.warning(f"Error processing image {filename}: {e}")

    # Step 4: Return the best match details
    if best_match_filename:
        st.success(f"Best match found: {best_match_filename} with score {best_score:.2f}")
    else:
        st.warning("No matching faces found in the folder.")

    return best_match_filename, best_score, image1_with_faces



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


    
def resize_image(image, target_size=250):
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
        student_info = txt_file.read()
    return student_info
    
def compare_faces(image1, image2):
    # Assuming face_detector is already defined and loaded
    face_detector.setInputSize([image1.shape[1], image1.shape[0]])
    faces1 = face_detector.infer(image1)

    face_detector.setInputSize([image2.shape[1], image2.shape[0]])
    faces2 = face_detector.infer(image2)

    # Check if faces are detected and unpack properly
    if len(faces1) == 0 or len(faces2) == 0:
        st.warning("No faces detected.")
        return None

    # Draw bounding boxes on the images based on the detected faces
    image1_with_boxes = draw_bounding_boxes(image1, faces1)
    image2_with_boxes = draw_bounding_boxes(image2, faces2)

    # Display the images with bounding boxes
    st.image(image1_with_boxes / 255.0, caption="Image 1 with Detected Faces", use_column_width=True)
    st.image(image2_with_boxes / 255.0, caption="Image 2 with Detected Faces", use_column_width=True)

    # Calculate and return the similarity score
    score = calculate_similarity(faces1, faces2)
    return score


def draw_bounding_boxes(image, faces):
    for face in faces:
        # Đảm bảo face có ít nhất 4 giá trị và ép kiểu chúng thành số nguyên
        if len(face) >= 4:
            x, y, w, h = map(int, face[:4])  # Ép kiểu tọa độ thành số nguyên
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image




def run_app5():
    """Phần 1: Tìm khuôn mặt giống nhất trong thư mục."""
    
    st.title("Tìm thông tin khuôn mặt trong lớp")

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_image is not None:
        folder_path = "Face_Verification/image"  # Đường dẫn thư mục
        if os.path.isdir(folder_path):
            st.write(f"Finding similar faces in the folder: {folder_path}")
            best_match_filename, best_score, processed_image = find_similar_faces(uploaded_image, folder_path)

            # Hiển thị hình ảnh đã xử lý với khuôn mặt được phát hiện
            #st.image(cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), caption="Processed Image with Detected Faces", use_column_width=True)

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
    st.header("So sánh ảnh chân dung và ảnh thẻ")
    uploaded_image1 = st.file_uploader("Upload Portrait Image...", type=["jpg", "jpeg", "png"], key="portrait")
    uploaded_image2 = st.file_uploader("Upload ID Image...", type=["jpg", "jpeg", "png"], key="id")

    if uploaded_image1 and uploaded_image2:
        image1 = Image.open(uploaded_image1).convert("RGB")
        image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    
        image2 = Image.open(uploaded_image2).convert("RGB")
        image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)
        face_img1 = extract_face(image1)
        if face_img1 is not None:
            st.image(cv2.cvtColor(face_img1, cv2.COLOR_BGR2RGB), caption="Ảnh khuôn mặt")
        else:
            st.warning("Không tìm thấy khuôn mặt trong ảnh thẻ. Vui lòng thử lại với một ảnh khác.")
            
        face_img2 = extract_face_the_sv(image2)
        if face_img2 is not None:
            st.image(cv2.cvtColor(face_img2, cv2.COLOR_BGR2RGB), caption="Ảnh khuôn mặt")
        else:
            st.warning("Không tìm thấy khuôn mặt trong ảnh thẻ. Vui lòng thử lại với một ảnh khác.")
        
         st.write(f"{calculate_similarity(face_img1, face_img2)}")
    
        
if __name__ == "__main__":
    run_app5()
