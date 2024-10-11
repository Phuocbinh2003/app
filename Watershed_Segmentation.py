import streamlit as st
import cv2 as cv
import os

# Hàm để resize ảnh sao cho chiều cao của chúng bằng nhau
def resize_image(image, target_height):
    h, w = image.shape[:2]
    scaling_factor = target_height / h
    new_width = int(w * scaling_factor)
    resized_image = cv.resize(image, (new_width, target_height))
    return resized_image

# Hàm cho ứng dụng thứ 2
def run_app2():
    st.title('✨ Ứng dụng phân đoạn ký tự biển số ✨')

    # Danh sách các đường dẫn tới các hình ảnh bước và kết quả
    practice_steps_image_paths = [
        "my_folder/Buoc_test1.png",  # Bước 1
        "my_folder/Buoc_test2.png"   # Bước 2
    ]

    result_image_paths = [
        "my_folder/KQ_test1.png",    # Kết quả 1
        "my_folder/KQ_test2.png"     # Kết quả 2
    ]

    # Hiển thị từng cặp ảnh thực hành và kết quả
    for step_image_path, result_image_path in zip(practice_steps_image_paths, result_image_paths):
        st.write("### Bước thực hành")
        col1, col2 = st.columns([1, 1])

        with col1:
            if os.path.exists(step_image_path):
                img_step = cv.imread(step_image_path)

                if img_step is not None:
                    st.image(img_step, caption='Bước thực hành', use_column_width=True)
            else:
                st.error(f"Không tìm thấy ảnh: {step_image_path}")

        with col2:
            st.write("### Kết quả")
            if os.path.exists(result_image_path):
                img_result = cv.imread(result_image_path)

                if img_step is not None and img_result is not None:
                    img_result_resized = resize_image(img_result, img_step.shape[0])
                    st.image(img_result_resized, caption='Kết quả', use_column_width=True)
            else:
                st.error(f"Không tìm thấy ảnh: {result_image_path}")

if __name__ == "__main__":
    run_app2()
