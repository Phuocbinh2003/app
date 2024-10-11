import streamlit as st
import cv2 as cv
import os

# Hàm cho ứng dụng thứ 2
def run_app2():
    st.title('✨ Ứng dụng phân đoạn ký tự biển số ✨')

    # Danh sách các đường dẫn tới các hình ảnh train
    train_image_paths = [
        "my_folder/Buoc_test1.png",
        "my_folder/Buoc_test2.png",
        "my_folder/KQ_test1.png",
        "my_folder/KQ_test2.png"
    ]

    # Hiển thị lần lượt 4 ảnh train
    st.header("1. Ảnh Train và Kết quả")

    for train_image_path in train_image_paths:
        if os.path.exists(train_image_path):
            img_np = cv.imread(train_image_path)

            if img_np is not None:
                st.image(img_np, caption='Train Image', use_column_width=True)
        else:
            st.error(f"Không tìm thấy ảnh: {train_image_path}")

if __name__ == "__main__":
    run_app2()
