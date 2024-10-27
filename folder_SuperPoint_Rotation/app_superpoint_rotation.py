# app.py
import streamlit as st
from PIL import Image

# Streamlit UI
st.title("So sánh các mô hình phát hiện đặc trưng: SIFT, ORB, và SuperPoint")

st.header("1. Giới thiệu dữ liệu")
st.write("Dataset là nhưng ảnh trong tập Synthetic Shapes Dataset sao cho SIFT hoặc ORB đạt 100% về phát hiện Keypoints (theo Ground Truth)")
data=''

# Đường dẫn tới các ảnh đã xử lý
sift_image_path = 'processed_images/sift_result.png'
orb_image_path = 'processed_images/orb_result.png'
superpoint_image_path = 'processed_images/superpoint_result.png'

# Hiển thị ảnh SIFT
st.header("2. Hiển thị kết quả mô hình")
st.subheader("2.1. Mô hình SIFT")
sift_image = Image.open(sift_image_path)
st.image(sift_image, caption="Ảnh với đặc trưng SIFT", use_column_width=True)
st.write("**Nhận xét:** Mô hình SIFT phát hiện các đặc trưng mạnh mẽ trong ảnh, đặc biệt hiệu quả với các góc cạnh và các chi tiết phức tạp.")

# Hiển thị ảnh ORB
st.subheader("2.2. Mô hình ORB")
orb_image = Image.open(orb_image_path)
st.image(orb_image, caption="Ảnh với đặc trưng ORB", use_column_width=True)
st.write("**Nhận xét:** Mô hình ORB nhanh và hiệu quả, đặc biệt phù hợp cho các ứng dụng thời gian thực nhưng có thể bỏ qua một số đặc trưng chi tiết so với SIFT.")

# Hiển thị ảnh SuperPoint
st.subheader("2.3. Mô hình SuperPoint")
superpoint_image = Image.open(superpoint_image_path)
st.image(superpoint_image, caption="Ảnh với đặc trưng SuperPoint", use_column_width=True)
st.write("**Nhận xét:** Mô hình SuperPoint hoạt động tốt với các đặc trưng chính trong ảnh và có hiệu quả cao trong việc phát hiện đặc trưng cho các ứng dụng yêu cầu khả năng phát hiện trong môi trường thay đổi.")
