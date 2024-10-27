import streamlit as st
import cv2
import numpy as np
from matplotlib import pyplot as plt
st.title("So sánh các mô hình phát hiện đặc trưng: SIFT, ORB, và SuperPoint")

st.header("1. Giới thiệu dữ liệu")
st.write("Ứng dụng này sử dụng một ảnh mẫu để kiểm tra khả năng phát hiện đặc trưng và độ ổn định khi xoay ảnh của các mô hình SIFT, ORB và SuperPoint.")

uploaded_image = st.file_uploader("Tải lên ảnh của bạn:", type=["jpg", "png", "jpeg"])
if uploaded_image:
    image = load_image(uploaded_image)

    st.header("2. So sánh các mô hình phát hiện đặc trưng")

    st.subheader("2.1. Mô hình SIFT")
    if st.checkbox("Hiển thị đặc trưng SIFT"):
        keypoints, descriptors = detect_keypoints_sift(image)
        plot_keypoints(image, keypoints, title="SIFT Keypoints")
        st.write("**Biểu đồ SIFT**")
        evaluate_model(image, detect_keypoints_sift, "SIFT Keypoints vs Rotation Angle")

    st.subheader("2.2. Mô hình ORB")
    if st.checkbox("Hiển thị đặc trưng ORB"):
        keypoints, descriptors = detect_keypoints_orb(image)
        plot_keypoints(image, keypoints, title="ORB Keypoints")
        st.write("**Biểu đồ ORB**")
        evaluate_model(image, detect_keypoints_orb, "ORB Keypoints vs Rotation Angle")

    st.subheader("2.3. Mô hình SuperPoint")
    if st.checkbox("Hiển thị đặc trưng SuperPoint"):
        keypoints, descriptors = detect_keypoints_superpoint(image)
        # SuperPoint output needs handling since it's in numpy format
        st.write("SuperPoint detected keypoints")
        st.write(keypoints)
        st.write("**Biểu đồ SuperPoint**")
        evaluate_model(image, detect_keypoints_superpoint, "SuperPoint Keypoints vs Rotation Angle")
