import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import requests
# Hàm cho ứng dụng thứ 2
def run_app2():
    st.title('✨ Ứng dụng phân đoạn ký tự biển số ✨')

    # Danh sách các URL hoặc đường dẫn tới các hình ảnh train
    train_image_urls = [
        "my_folder/Buoc_test1.png",
        "my_folder/Buoc_test2.png",
        "my_folder/KQ_test1.png",
        "my_folder/KQ_test2.png"
    ]

    # Hiển thị lần lượt 4 ảnh train
    st.header("1. Ảnh Train và Kết quả")

    for train_image_url in train_image_urls:
        # Tải ảnh từ URL
        image_response = requests.get(train_image_url)
        nparr = np.frombuffer(image_response.content, np.uint8)
        img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)

        if img_np is not None:
            st.image(img_np, caption='Train Image', use_column_width=True)

if __name__ == "__main__":
    run_app2()
