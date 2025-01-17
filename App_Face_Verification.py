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


def visualize_matches(img1, faces1, img2, faces2, matches, scores, target_size=[512, 512]): # target_size: (h, w)
    out1 = img1.copy()
    out2 = img2.copy()
    matched_box_color = (0, 255, 0)    # BGR
    mismatched_box_color = (0, 0, 255) # BGR

    # Resize to 256x256 with the same aspect ratio
    padded_out1 = np.zeros((target_size[0], target_size[1], 3)).astype(np.uint8)
    h1, w1, _ = out1.shape
    ratio1 = min(target_size[0] / out1.shape[0], target_size[1] / out1.shape[1])
    new_h1 = int(h1 * ratio1)
    new_w1 = int(w1 * ratio1)
    resized_out1 = cv2.resize(out1, (new_w1, new_h1), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    top = max(0, target_size[0] - new_h1) // 2
    bottom = top + new_h1
    left = max(0, target_size[1] - new_w1) // 2
    right = left + new_w1
    padded_out1[top : bottom, left : right] = resized_out1

    # Draw bbox
    bbox1 = faces1[0][:4] * ratio1
    x, y, w, h = bbox1.astype(np.int32)
    cv2.rectangle(padded_out1, (x + left, y + top), (x + left + w, y + top + h), matched_box_color, 2)

    # Resize to 256x256 with the same aspect ratio
    padded_out2 = np.zeros((target_size[0], target_size[1], 3)).astype(np.uint8)
    h2, w2, _ = out2.shape
    ratio2 = min(target_size[0] / out2.shape[0], target_size[1] / out2.shape[1])
    new_h2 = int(h2 * ratio2)
    new_w2 = int(w2 * ratio2)
    resized_out2 = cv2.resize(out2, (new_w2, new_h2), interpolation=cv2.INTER_LINEAR).astype(np.float32)
    top = max(0, target_size[0] - new_h2) // 2
    bottom = top + new_h2
    left = max(0, target_size[1] - new_w2) // 2
    right = left + new_w2
    padded_out2[top : bottom, left : right] = resized_out2

    # Draw bbox
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

            image2_resized = image2
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
    


def draw_bounding_boxes(image, faces):
    for face in faces:
        # Đảm bảo face có ít nhất 4 giá trị và ép kiểu chúng thành số nguyên
        if len(face) >= 4:
            x, y, w, h = map(int, face[:4])  # Ép kiểu tọa độ thành số nguyên
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

def compare_faces(image1, image2, target_size=[512, 512]):
    """
    So sánh khuôn mặt giữa hai ảnh và vẽ kết quả lên ảnh.

    Args:
    - image1_path: Đường dẫn đến ảnh đầu tiên.
    - image2_path: Đường dẫn đến ảnh thứ hai.
    - face_detector: Mô hình nhận diện khuôn mặt (YuNet).
    - face_recognizer: Mô hình nhận diện khuôn mặt cho việc so sánh (SFace).
    - target_size: Kích thước mục tiêu để thay đổi kích thước ảnh.

    Returns:
    - image: Ảnh kết quả với các hộp giới hạn khuôn mặt và điểm số so sánh.
    """
    
    # Đọc ảnh và chuyển sang định dạng BGR
    image1 = cv2.cvtColor(np.array(image1), cv2.COLOR_RGB2BGR)
    image1=resize_image(image1)

    image2 = cv2.cvtColor(np.array(image2), cv2.COLOR_RGB2BGR)

    # Nhận diện khuôn mặt từ ảnh 1
    face_detector.setInputSize([image1.shape[1], image1.shape[0]])
    faces1 = face_detector.infer(image1)
    
    # Nhận diện khuôn mặt từ ảnh 2
    face_detector.setInputSize([image2.shape[1], image2.shape[0]])
    faces2 = face_detector.infer(image2)

    # Nếu không phát hiện khuôn mặt, trả về cảnh báo
    if len(faces1) == 0 or len(faces2) == 0:
        return "Không tìm thấy khuôn mặt trong ít nhất một ảnh. Vui lòng thử lại."

    # So sánh khuôn mặt giữa ảnh 1 và ảnh 2 bằng SFace
    scores = []
    matches = []
    for face in faces2:
        # So sánh với khuôn mặt đầu tiên từ ảnh 1
        result = face_recognizer.match(image1, faces1[0][:-1], image2, face[:-1])  # So sánh khuôn mặt
        scores.append(result[0])
        matches.append(result[1])

    # Vẽ các hộp giới hạn và kết quả lên ảnh
    image = visualize_matches(image1, faces1, image2, faces2, matches, scores, target_size)
    
    return image



def run_app5():
    """Phần 1: Tìm khuôn mặt giống nhất trong thư mục."""
    
    st.title("Tìm thông tin khuôn mặt trong lớp")
    st.markdown("""
    1. **Chọn ảnh cần so sánh**: Tải lên **ảnh chân dung** của bạn. Hệ thống sẽ tìm khuôn mặt trong ảnh và so sánh với ảnh học sinh trong thư mục.
    2. **Kết quả tìm kiếm**: Ứng dụng sẽ hiển thị thông tin học sinh có khuôn mặt giống với ảnh của bạn, bao gồm tên, mã sinh viên, lớp học...
    3. **Không tìm thấy kết quả**: Nếu không có khuôn mặt giống, hệ thống sẽ cảnh báo không tìm thấy khuôn mặt phù hợp.
    """)
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
    st.markdown("""
    
    1. **Tải ảnh chân dung và ảnh thẻ**: Tải lên **hai ảnh** của bạn. Một là ảnh chân dung và một là ảnh thẻ.
    2. **So sánh khuôn mặt**: Ứng dụng sẽ so sánh khuôn mặt trong hai ảnh và hiển thị kết quả.
    3. **Kết quả so sánh**: Nếu khuôn mặt giống nhau, bạn sẽ thấy kết quả so sánh và ảnh đã được xử lý.
    4. **Không giống nhau**: Nếu khuôn mặt trong hai ảnh khác nhau, hệ thống sẽ cảnh báo.
    """)
    uploaded_image1 = st.file_uploader("Upload Portrait Image...", type=["jpg", "jpeg", "png"], key="portrait")
    uploaded_image2 = st.file_uploader("Upload ID Image...", type=["jpg", "jpeg", "png"], key="id")

    if uploaded_image1 and uploaded_image2:
        # Đọc ảnh và chuyển đổi thành định dạng PIL
        image1 = Image.open(uploaded_image1).convert("RGB")
        image2 = Image.open(uploaded_image2).convert("RGB")
        
        # Gọi hàm để so sánh khuôn mặt
        result_image = compare_faces(image1, image2)
    
        # Kiểm tra kết quả trả về từ hàm compare_faces
        if isinstance(result_image, str):  # Nếu là chuỗi, có thể là thông báo lỗi
            st.error(result_image)
        else:
            st.image(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB), caption="Kết quả so sánh khuôn mặt", use_column_width=True)

                  
  
        
       
        
    
        
if __name__ == "__main__":
    run_app5()
