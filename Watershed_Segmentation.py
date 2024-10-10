import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image
import requests
import matplotlib.pyplot as plt


# Hàm cho ứng dụng thứ 2
def run_app2():
    st.title('✨ Ứng dụng phân đoạn ký tự biển số ✨')

    # Danh sách các URL hoặc đường dẫn tới các hình ảnh train và test
    train_image_urls = [
        "my_folder/Buoc_test1.png",
        "my_folder/Buoc_test2.png"
    ]
    
    test_image_urls = [
        "my_folder/KQ_test1.png",
        "my_folder/KQ_test2.png.jpg"
    ]

    # Hiển thị lần lượt ảnh train và kết quả
    st.header("1. Ảnh Train và Kết quả")


if __name__ == "__main__":
    run_app2()
