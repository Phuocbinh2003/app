import streamlit as st
import cv2
import numpy as np
from video_upload import process_video

# Tiêu đề của ứng dụng
st.title("1.Object Tracking Using KCF ")

st.markdown("""
    KCF là một thuật toán theo dõi đối tượng mạnh mẽ, có thể theo dõi đối tượng trong video với hiệu suất cao và độ chính xác tốt. KCF sử dụng bộ lọc kernel để xác định đối tượng trong mỗi frame của video.
""")


st.title("2.ví dụ minh họa")
# Tải video lên
video_file = st.file_uploader("Tải video của bạn (MP4)", type=["mp4", "avi"])

if video_file is not None:
    # Hiển thị video tải lên
    st.video(video_file)
st.title("3. thảo luận ")

 - **Background Clutters**: Nền có nhiều chuyển động hoặc đối tượng không liên quan có thể gây nhiễu cho thuật toán.
- **Illumination Variations**: Sự thay đổi ánh sáng mạnh có thể ảnh hưởng đến độ chính xác của thuật toán.
- **Occlusion**: Khi đối tượng bị che khuất hoàn toàn, thuật toán có thể mất dấu đối tượng.
- **Fast Motion**: Đối tượng di chuyển quá nhanh có thể khiến thuật toán không kịp cập nhật vị trí chính xác.
  

