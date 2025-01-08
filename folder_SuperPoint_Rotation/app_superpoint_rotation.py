# app.py
import streamlit as st
from PIL import Image

def run_app7():
    # Giao diện Streamli
    st.title("So sánh các mô hình phát hiện đặc trưng: SIFT, ORB, và SuperPoint")

    st.header("1. Giới thiệu dữ liệu")
    st.write("Dataset là những ảnh trong tập Synthetic Shapes Dataset để kiểm tra hiệu quả phát hiện Keypoints của các mô hình SIFT và ORB.")

    # Hiển thị ảnh dataset mẫu
    dataset_image_path = 'folder_SuperPoint_Rotation/2710.png'
    dataset_image = Image.open(dataset_image_path)
    st.image(dataset_image, caption="Dataset", use_column_width=True)
    st.write("Tổng cộng có 166 ảnh SIFT và 330 ảnh ORB đạt 100% phát hiện Keypoints theo Ground Truth.")

    # Đường dẫn tới các ảnh đã xử lý
    sift_image_path1 = 'folder_SuperPoint_Rotation/xoay1.png'
    
    orb_image_path1 = 'folder_SuperPoint_Rotation/xoay2.png'
    
    superpoint_image_path1 = 'folder_SuperPoint_Rotation/XOAY3.png'
   
     st.header("2. Đánh giá Matching Keypoint")

    st.write("""
    **Đánh giá Matching Keypoints với SIFT, ORB, và SuperPoint theo tiêu chí Rotation**
    
    Chúng ta tiến hành đánh giá độ chính xác của các mô hình SIFT, ORB, và SuperPoint trên các góc quay từ 0° đến 350° với bước nhảy 10°. Đối với mỗi mô hình, ta sử dụng Brute-Force Matching với các tham số khác nhau để so sánh các keypoints được phát hiện và các keypoints ground truth.
    
    1. **Mô hình SIFT**: 
        - Sử dụng Brute-Force Matching với normType = cv2.NORM_L2 (Euclidean distance) để tính toán khoảng cách giữa các descriptor.
        - Áp dụng Lowe's ratio test với tỷ lệ 0.75 để giảm thiểu các keypoint matching yếu.
        - Đo độ chính xác bằng tỷ lệ số keypoints matching đúng so với tổng số keypoints trong ground truth.
        
    2. **Mô hình ORB**: 
        - Sử dụng Brute-Force Matching với normType = cv2.NORM_HAMMING (Hamming distance) và crossCheck = True để chỉ lấy các keypoint matching hai chiều.
        - Đo độ chính xác tương tự như SIFT.
    
    3. **Mô hình SuperPoint**:
        - Sử dụng Brute-Force Matching với normType = cv2.NORM_L2 (Euclidean distance) và Lowe's ratio test với tỷ lệ 0.75.
        - Đo độ chính xác như mô hình SIFT.
    
    Đánh giá sẽ được thực hiện trên các góc quay từ 0° đến 350° với bước nhảy 10°, và ta sẽ tính toán tỷ lệ accuracy cho từng mô hình.
    """)
    # Phần SIFT
    st.header("3. Hiển thị kết quả mô hình")
    st.subheader("2.1. Mô hình SIFT")
    sift_image1 = Image.open(sift_image_path1)
    st.image(sift_image1, caption="Ảnh với đặc trưng SIFT", use_column_width=True)
    
    st.write("**Nhận xét:** Mô hình SIFT phát hiện các đặc trưng mạnh mẽ, đặc biệt hiệu quả với các góc cạnh và chi tiết phức tạp. Nhưng độ chính xác rất thấp với các điểm đúng nên xoay sẽ ảnh hưởng lớn đến độ chính xác")
    sift_imagebd = Image.open(sift_image_pathbd)
  

    # Phần ORB
    st.subheader("2.2. Mô hình ORB")
    orb_image1 = Image.open(orb_image_path1)
    st.image(orb_image1, caption="Ảnh với đặc trưng ORB", use_column_width=True)
    
    st.write("**Nhận xét:** Mô hình ORB nhanh và hiệu quả, đặc biệt thích hợp cho các ứng dụng thời gian thực, nhưng bỏ qua một số đặc trưng chi tiết so với SIFT.")


    # Phần SuperPoint
    st.subheader("2.3. Mô hình SuperPoint")
    superpoint_image1 = Image.open(superpoint_image_path1)
    st.image(superpoint_image1, caption="Ảnh với đặc trưng SuperPoint", use_column_width=True)
   
    st.write("Với SuperPoint, số lượng đặc trưng phát hiện và số đặc trưng tương đồng duy trì ổn định qua các biến đổi xoay.")
    
# Chạy ứng dụng
if __name__ == "__main__":
    run_app7()
