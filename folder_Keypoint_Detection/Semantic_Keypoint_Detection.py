import streamlit as st
import pandas as pd
import cv2
from PIL import Image
import matplotlib.pyplot as plt

def run_app6():
    # Phần 1: Synthetic Shapes Dataset
    st.header("1. Synthetic Shapes Dataset")
    img1 = Image.open("folder_Keypoint_Detection/Untitled.png")
    st.image(img1, caption="Synthetic Shapes Dataset Example", use_column_width=True)
    st.markdown("Bộ dữ liệu bao gồm tổng cộng 9.028 hình ảnh, mỗi hình đều được gắn kèm các điểm đặc trưng chính xác")
    
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

    # Phần 3: Biểu đồ so sánh độ đo Precision và Recall của SIFT và ORB
    st.header("3. Precision and Recall Comparison Chart for SIFT and ORB")

    # Dữ liệu cho biểu đồ
    data = {
        "Method": ["draw_stripes - SIFT", "draw_lines - SIFT", "draw_polygon - SIFT", 
                   "draw_ellipses - SIFT", "draw_cube - SIFT", "gaussian_noise - SIFT", 
                   "draw_checkerboard - SIFT", "draw_star - SIFT", "draw_multiple_polygons - SIFT",
                   "draw_stripes - ORB", "draw_lines - ORB", "draw_polygon - ORB", 
                   "draw_ellipses - ORB", "draw_cube - ORB", "gaussian_noise - ORB", 
                   "draw_checkerboard - ORB", "draw_star - ORB", "draw_multiple_polygons - ORB"],
        "Precision": [0.2004, 0.4995, 0.1429, 0.0000, 0.2513, 0.0000, 0.1498, 0.4431, 0.2646,
                      0.0934, 0.4135, 0.4172, 0.0000, 0.3446, 0.0000, 0.2075, 0.3706, 0.3307],
        "Recall": [0.2519, 0.7348, 0.1393, 0.0000, 0.4274, 0.0000, 0.1760, 0.7603, 0.3411,
                   0.0640, 0.2559, 0.5417, 0.0000, 0.5120, 0.0000, 0.3949, 0.6244, 0.3202]
    }
    
    df = pd.DataFrame(data)

    # Tạo biểu đồ cột cho Precision và Recall
    fig, ax = plt.subplots(figsize=(10, 6))
    df.set_index("Method")[["Precision", "Recall"]].plot(kind='bar', ax=ax)
    ax.set_title("Precision and Recall for SIFT and ORB")
    ax.set_ylabel("Score")
    ax.set_xlabel("Methods")
    ax.axhline(0, color='grey', lw=1)
    ax.legend(title='Metrics')
    st.pyplot(fig)  # Hiển thị biểu đồ trong Streamlit

if __name__ == "__main__":
    run_app6()
