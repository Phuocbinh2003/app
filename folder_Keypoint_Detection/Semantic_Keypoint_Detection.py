import streamlit as st
import pandas as pd
import cv2
from PIL import Image

def run_app6():
    # Phần 1: Synthetic Shapes Dataset
    st.header("1. Synthetic Shapes Dataset")
    img1 = Image.open("folder_Keypoint_Detection/PR.png")
    st.image(img1, caption="Synthetic Shapes Dataset Example", use_column_width=True)
    
    # Phần 2: Giới thiệu về Precision và Recall
    st.header("2. Precision and Recall")
    
    st.markdown("""
    - **Precision** là tỉ lệ giữa số lượng dự đoán đúng (True Positives) và tổng số dự đoán (True Positives + False Positives).
    - **Recall** (hoặc Tỉ lệ phát hiện) là tỉ lệ giữa số lượng dự đoán đúng và tổng số thực sự (True Positives + False Negatives).
    """)
    
    # Công thức cho Precision và Recall
    st.latex(r"""
    \text{Precision} = \frac{TP}{TP + FP}
    """)
    st.latex(r"""
    \text{Recall} = \frac{TP}{TP + FN}
    """)
    
    # Hình minh họa Precision và Recall
    img2 = Image.open("folder_Keypoint_Detection/PR.png")
    st.image(img2, caption="Precision and Recall Diagram", use_column_width=True)
    
    # Phần 3: Bảng so sánh độ đo Precision và Recall của SIFT và ORB
    st.header("3. Precision and Recall Comparison Table for SIFT and ORB")
    
    # Tạo bảng dữ liệu Precision và Recall cho SIFT và ORB
    data = {
        "Method": ["SIFT", "ORB"],
        "Precision": [0.85, 0.75],  # Dữ liệu mẫu
        "Recall": [0.80, 0.70]      # Dữ liệu mẫu
    }
    
    df = pd.DataFrame(data)
    
    # Hiển thị bảng dữ liệu
    st.table(df)
    
    # Hình ảnh bảng so sánh Precision và Recall
    img3 = Image.open("images/precision_recall_table.png")
    st.image(img3, caption="Precision and Recall Table for SIFT and ORB", use_column_width=True)

if __name__ == "__main__":
    run_app6()
