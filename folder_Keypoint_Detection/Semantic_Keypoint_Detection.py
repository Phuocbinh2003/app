import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def run_app6():
    # Part 1: Synthetic Shapes Dataset
    st.header("1. Synthetic Shapes Dataset")
    img1 = Image.open("folder_Keypoint_Detection/Untitled.png")
    st.image(img1, caption="Synthetic Shapes Dataset Example", use_column_width=True)
    st.markdown("Bộ dữ liệu bao gồm tổng cộng 9.028 hình ảnh, mỗi hình đều được gắn kèm các điểm đặc trưng chính xác")
    
    # Part 2: Introduction to Precision and Recal
    st.header("2. Precision and Recall")
    
    st.markdown("""
    - **Precision** là tỉ lệ giữa số lượng dự đoán đúng (True Positives) và tổng số dự đoán (True Positives + False Positives).
    - **Recall** (hoặc Tỉ lệ phát hiện) là tỉ lệ giữa số lượng dự đoán đúng và tổng số thực sự (True Positives + False Negatives).
    """)
    
    # Precision and Recall Diagram
    img2 = Image.open("folder_Keypoint_Detection/PR.png")
    st.image(img2, caption="Precision and Recall Diagram", use_column_width=True)
    
    # Công thức cho Precision và Recall
 

    
    st.header("3. Phương pháp")
    img1 = Image.open("folder_Keypoint_Detection/download.png")
    st.image(img1, caption="Synthetic Shapes Dataset Example", use_column_width=True)

    st.markdown("""
    Việc xác định các độ đo Precision và Recall của SIFT và ORB trong bài này được thực hiện bằng cách so sánh đặc trưng SIFT và ORB với các đặc trưng thực tế trong tệp points.
    
    - **True Positives (TP)**: Số lượng điểm đặc trưng được phát hiện nằm trong một bán kính cho trước từ các điểm đặc trưng thực tế.
    - **False Positives (FP)**: Số lượng điểm đặc trưng được phát hiện nhưng không khớp với bất kỳ điểm thực tế nào trong bán kính đã định. Nghĩa là, khoảng cách từ điểm được phát hiện đến tất cả các điểm thực tế đều lớn hơn ngưỡng đã đặt.
    - **False Negatives (FN)**: Số lượng điểm thực tế không có điểm phát hiện nào nằm trong bán kính cho trước xung quanh nó, tức là không có điểm phát hiện nào gần với điểm thực tế đó.
    """)
    # Part 3: Precision and Recall Comparison for SIFT and ORB
    st.header("4. Precision and Recall Comparison for SIFT and ORB")

    # Data setup for shapes with SIFT and ORB methods
    data = {
        "Shape": ["stripes", "lines", "polygon", "ellipses", "cube", 
                  "gaussian_noise", "checkerboard", "star", "multiple_polygons"],
        "SIFT_Precision": [0.2004, 0.4995, 0.1429, 0.0000, 0.2513, 0.0000, 0.1498, 0.4431, 0.2646],
        "SIFT_Recall": [0.2519, 0.7348, 0.1393, 0.0000, 0.4274, 0.0000, 0.1760, 0.7603, 0.3411],
        "ORB_Precision": [0.0934, 0.4135, 0.4172, 0.0000, 0.3446, 0.0000, 0.2075, 0.3706, 0.3307],
        "ORB_Recall": [0.0640, 0.2559, 0.5417, 0.0000, 0.5120, 0.0000, 0.3949, 0.6244, 0.3202]
    }
    
    df = pd.DataFrame(data)
    x = np.arange(len(df["Shape"]))  # X-axis locations for shapes
    width = 0.35  # Width of the bars

    # Create the grouped bar chart for Precision
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Precision grouped bars
    ax1.bar(x - width/2, df["SIFT_Precision"], width, label="SIFT", color='orange')
    ax1.bar(x + width/2, df["ORB_Precision"], width, label="ORB", color='blue')
    ax1.set_xticks(x)
    ax1.set_xticklabels(df["Shape"], rotation=45, ha="right")
    ax1.set_title("4.1 Đánh giá dựa trên độ đo Precision")
    ax1.set_xlabel("")
    ax1.set_ylabel("Precision Score")
    ax1.legend()

    # Recall grouped bars
    ax2.bar(x - width/2, df["SIFT_Recall"], width, label="SIFT", color='orange')
    ax2.bar(x + width/2, df["ORB_Recall"], width, label="ORB", color='blue')
    ax2.set_xticks(x)
    ax2.set_xticklabels(df["Shape"], rotation=45, ha="right")
    ax2.set_title("4.2 Đánh giá dựa trên độ đo Recall")
    ax2.set_xlabel("")
    ax2.set_ylabel("Recall Score")
    ax2.legend()

    # Display the plots in Streamlit
    st.pyplot(fig)
    st.header("5. Nhận xét")
    st.markdown(
    """
    ### Nhận Xét về SIFT
    - **Hiệu suất tốt trên một số hình dạng**: SIFT đạt kết quả Precision và Recall cao đối với các hình như `lines`, `star`, và `draw_cube`, nhưng lại cho hiệu suất kém với `draw_ellipses` và `gaussian_noise` (cả Precision và Recall bằng 0).
    
    
    ### Nhận Xét về ORB
   
    """

          
      )
if __name__ == "__main__":
    run_app6()
