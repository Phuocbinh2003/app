import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

def run_app6():
    # Phần 1: Synthetic Shapes Dataset
    st.header("1. Synthetic Shapes Dataset")
    img1 = Image.open("folder_Keypoint_Detection/Untitled.png")
    st.image(img1, caption="Synthetic Shapes Dataset Example", use_column_width=True)
    st.markdown("Bộ dữ liệu bao gồm tổng cộng 9.028 hình ảnh, mỗi hình đều được gắn kèm các điểm đặc trưng chính xác.")
    
    # Phần 2: Giới thiệu về Precision và Recall
    st.header("2. Precision and Recall")
    
    st.markdown("""
    - **Precision** là tỉ lệ giữa số lượng dự đoán đúng (True Positives) và tổng số dự đoán (True Positives + False Positives).
    - **Recall** (hoặc Tỉ lệ phát hiện) là tỉ lệ giữa số lượng dự đoán đúng và tổng số thực sự (True Positives + False Negatives).
    """)
    
    # Hình minh họa Precision và Recall
    img2 = Image.open("folder_Keypoint_Detection/PR.png")
    st.image(img2, caption="Precision and Recall Diagram", use_column_width=True)

    # Phần 3: Biểu đồ so sánh độ đo Precision và Recall của SIFT và ORB
    st.header("3. Precision and Recall Comparison Charts for SIFT and ORB")

    # Dữ liệu cho biểu đồ
    data = {
        "Method": ["SIFT", "ORB"],
        "Precision": [0.3411, 0.4075],  # Trung bình của Precision cho SIFT và ORB
        "Recall": [0.3295, 0.5744]      # Trung bình của Recall cho SIFT và ORB
    }
    
    df = pd.DataFrame(data)

    # Tạo hai biểu đồ cho Precision và Recall
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Biểu đồ Precision
    ax1.barh(df["Method"], df["Precision"], color=['orange', 'blue'])  # SIFT là màu cam, ORB là màu xanh
    ax1.set_title("4.1 Đánh giá dựa trên độ đo Precision")
    ax1.set_xlabel("Precision Score")
    ax1.axvline(0, color='grey', lw=1)

    # Biểu đồ Recall
    ax2.barh(df["Method"], df["Recall"], color=['orange', 'blue'])  # SIFT là màu cam, ORB là màu xanh
    ax2.set_title("4.2 Đánh giá dựa trên độ đo Recall")
    ax2.set_xlabel("Recall Score")
    ax2.axvline(0, color='grey', lw=1)

    # Hiển thị biểu đồ
    st.pyplot(fig)  # Hiển thị biểu đồ trong Streamlit

if __name__ == "__main__":
    run_app6()
