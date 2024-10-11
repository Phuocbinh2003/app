import streamlit as st
import cv2 as cv
import os

# Hàm cho ứng dụng thứ 2
def run_app2():
    st.title('✨ Ứng dụng phân đoạn ký tự biển số ✨')

    # Danh sách các đường dẫn tới các hình ảnh train và kết quả
    practice_steps_image_paths = [
        "my_folder/Buoc_test1.png",  # Bước 1
        "my_folder/Buoc_test2.png"   # Bước 2
    ]

    result_image_paths = [
        "my_folder/KQ_test1.png",    # Kết quả 1
        "my_folder/KQ_test2.png"     # Kết quả 2
    ]

    # Hiển thị từng cặp ảnh thực hành và kết quả
    st.header("1. Ảnh Train và Kết quả")

    for step_image_path, result_image_path in zip(practice_steps_image_paths, result_image_paths):
        col1, col2 = st.columns(2)

        # Hiển thị ảnh "Bước thực hành" ở cột 1
        with col1:
            if os.path.exists(step_image_path):
                img_np = cv.imread(step_image_path)

                if img_np is not None:
                    st.image(img_np, caption='Bước thực hành', use_column_width=True)
            else:
                st.error(f"Không tìm thấy ảnh: {step_image_path}")

        # Hiển thị ảnh "Kết quả" ở cột 2
        with col2:
            if os.path.exists(result_image_path):
                img_np = cv.imread(result_image_path)

                if img_np is not None:
                    st.image(img_np, caption='Kết quả', use_column_width=True)
            else:
                st.error(f"Không tìm thấy ảnh: {result_image_path}")

if __name__ == "__main__":
    run_app2()
