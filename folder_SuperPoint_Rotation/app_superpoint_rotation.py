# app.py
import streamlit as st
from PIL import Image

def run_app7():
    # Giao diện Streamlit
    st.title("So sánh các mô hình phát hiện đặc trưng: SIFT, ORB, và SuperPoint")

    st.header("1. Giới thiệu dữ liệu")
    st.write("Dataset là những ảnh trong tập Synthetic Shapes Dataset để kiểm tra hiệu quả phát hiện Keypoints của các mô hình SIFT và ORB.")

    # Hiển thị ảnh dataset mẫu
    dataset_image_path = 'folder_SuperPoint_Rotation/2710.png'
    dataset_image = Image.open(dataset_image_path)
    st.image(dataset_image, caption="Dataset", use_column_width=True)
    st.write("Tổng cộng có 166 ảnh SIFT và 330 ảnh ORB đạt 100% phát hiện Keypoints theo Ground Truth.")

    # Đường dẫn tới các ảnh đã xử lý
    sift_image_path1 = 'folder_SuperPoint_Rotation/sift1.png'
    sift_image_path2 = 'folder_SuperPoint_Rotation/sift2.png'
    sift_image_pathbd = 'folder_SuperPoint_Rotation/siftbd.png'
    orb_image_path1 = 'folder_SuperPoint_Rotation/orb1.png'
    orb_image_path2 = 'folder_SuperPoint_Rotation/orb2.png'
    orb_image_pathbd = 'folder_SuperPoint_Rotation/orbbd.png'
    # superpoint_image_path1 = 'folder_SuperPoint_Rotation/superpoint1.png'
    # superpoint_image_path2 = 'folder_SuperPoint_Rotation/superpoint2.png'
    # superpoint_image_pathbd = 'folder_SuperPoint_Rotation/superpointbd.png'

    # Phần SIFT
    st.header("2. Hiển thị kết quả mô hình")
    st.subheader("2.1. Mô hình SIFT")
    sift_image1 = Image.open(sift_image_path1)
    st.image(sift_image1, caption="Ảnh với đặc trưng SIFT", use_column_width=True)
    sift_image2 = Image.open(sift_image_path2)
    st.image(sift_image2, caption="So sánh các đặc trưng tương đồng", use_column_width=True)
    st.write("**Nhận xét:** Mô hình SIFT phát hiện các đặc trưng mạnh mẽ, đặc biệt hiệu quả với các góc cạnh và chi tiết phức tạp.")
    sift_imagebd = Image.open(sift_image_pathbd)
    st.image(sift_imagebd, caption="Biểu đồ SIFT", use_column_width=True)
    st.write("Với SIFT, việc xoay ảnh làm thay đổi số lượng đặc trưng từ 20-30, nhưng các đặc trưng tương đồng ít thay đổi, trong khoảng từ 10-12.")

    # Phần ORB
    st.subheader("2.2. Mô hình ORB")
    orb_image1 = Image.open(orb_image_path1)
    st.image(orb_image1, caption="Ảnh với đặc trưng ORB", use_column_width=True)
    orb_image2 = Image.open(orb_image_path2)
    st.image(orb_image2, caption="So sánh các đặc trưng tương đồng", use_column_width=True)
    st.write("**Nhận xét:** Mô hình ORB nhanh và hiệu quả, đặc biệt thích hợp cho các ứng dụng thời gian thực, nhưng bỏ qua một số đặc trưng chi tiết so với SIFT.")
    orb_imagebd = Image.open(orb_image_pathbd)
    st.image(orb_imagebd, caption="Biểu đồ ORB", use_column_width=True)
    st.write("Với ORB, việc xoay ảnh làm tăng mạnh các đặc trưng (từ 23 đến 84), nhưng các đặc trưng tương đồng thay đổi ít, từ 10-20.")

    # # Phần SuperPoint
    # st.subheader("2.3. Mô hình SuperPoint")
    # superpoint_image1 = Image.open(superpoint_image_path1)
    # st.image(superpoint_image1, caption="Ảnh với đặc trưng SuperPoint", use_column_width=True)
    # superpoint_image2 = Image.open(superpoint_image_path2)
    # st.image(superpoint_image2, caption="So sánh các đặc trưng tương đồng", use_column_width=True)
    # st.write("**Nhận xét:** Mô hình SuperPoint có hiệu quả cao trong phát hiện đặc trưng chính trong ảnh, phù hợp cho môi trường thay đổi.")
    # superpoint_imagebd = Image.open(superpoint_image_pathbd)
    # st.image(superpoint_imagebd, caption="Biểu đồ SuperPoint", use_column_width=True)
    # st.write("Với SuperPoint, số lượng đặc trưng phát hiện và số đặc trưng tương đồng duy trì ổn định qua các biến đổi xoay.")

# Chạy ứng dụng
if __name__ == "__main__":
    run_app7()
