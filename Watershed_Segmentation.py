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

# Hàm cho ứng dụng
def run_app2():
    st.title('✨ Ứng dụng phân đoạn ký tự biển số ✨')

    # Đường dẫn tới các hình ảnh phần 1
    step_image_path_1 = "my_folder/Buoc_test1.png"
    result_image_path_1 = "my_folder/KQ_test1.png"

    step_image_path_2 = "my_folder/Buoc_test2.png"
    result_image_path_2 = "my_folder/KQ_test2.png"

    # Phần 1: Hiển thị cho 2 cặp ảnh đầu tiên (theo hàng dọc)
    st.header("1. Ảnh Train và Kết quả - Phần 1")

    st.write("### Bước thực hành 1")
    if os.path.exists(step_image_path_1):
        img_step_1 = cv.imread(step_image_path_1)
        if img_step_1 is not None:
            st.image(img_step_1, caption='Bước thực hành', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {step_image_path_1}")

    st.write("### Kết quả 1")
    if os.path.exists(result_image_path_1):
        img_result_1 = cv.imread(result_image_path_1)
        if img_step_1 is not None and img_result_1 is not None:
            img_result_1_resized = resize_image(img_result_1, img_step_1.shape[0])
            st.image(img_result_1_resized, caption='Kết quả', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {result_image_path_1}")

    st.write("### Bước thực hành 2")
    if os.path.exists(step_image_path_2):
        img_step_2 = cv.imread(step_image_path_2)
        if img_step_2 is not None:
            st.image(img_step_2, caption='Bước thực hành', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {step_image_path_2}")

    st.write("### Kết quả 2")
    if os.path.exists(result_image_path_2):
        img_result_2 = cv.imread(result_image_path_2)
        if img_step_2 is not None and img_result_2 is not None:
            img_result_2_resized = resize_image(img_result_2, img_step_2.shape[0])
            st.image(img_result_2_resized, caption='Kết quả', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {result_image_path_2}")

    # Đường dẫn tới các hình ảnh phần 2 (chỉ 2 ảnh)
    step_image_path_3 = "my_folder/KQ1.png"
    result_image_path_3 = "my_folder/KQ2.png"

    # Phần 2: Hiển thị cho 1 cặp ảnh tiếp theo (theo hàng dọc)
    st.header("2. Ảnh Train và Kết quả - Phần 2")

    st.write("### Bước thực hành 3")
    if os.path.exists(step_image_path_3):
        img_step_3 = cv.imread(step_image_path_3)
        if img_step_3 is not None:
            st.image(img_step_3, caption='Kết quả', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {step_image_path_3}")

    st.write("### Kết quả 3")
    if os.path.exists(result_image_path_3):
        img_result_3 = cv.imread(result_image_path_3)
        if img_step_3 is not None and img_result_3 is not None:
            img_result_3_resized = resize_image(img_result_3, img_step_3.shape[0])
            st.image(img_result_3_resized, caption='Kết quả', use_column_width=True)
    else:
        st.error(f"Không tìm thấy ảnh: {result_image_path_3}")

if __name__ == "__main__":
    run_app2()
