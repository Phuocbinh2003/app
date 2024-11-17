import streamlit as st
import cv2
import os



def run_app9():
    # Tiêu đề của ứng dụng
    st.title("1. Object Tracking Using KCF")
    
    st.markdown("""
        KCF (Kernelized Correlation Filters) là một thuật toán theo dõi đối tượng mạnh mẽ, có thể theo dõi đối tượng trong video với hiệu suất cao và độ chính xác tốt. KCF sử dụng bộ lọc kernel để xác định đối tượng trong mỗi frame của video.
    """)
    
    # Ví dụ minh họa
    st.title("2. Ví dụ minh họa")
    
    # Đường dẫn video có sẵn trong thư mục
    video_path = "videos/your_video.mp4"  # Thay thế 'your_video.mp4' bằng tên video của bạn trong thư mục 'videos'
    
    # Kiểm tra xem video có tồn tại hay không
    if os.path.exists(video_path):
        # Hiển thị video từ thư mục
        st.video(video_path)
    else:
        st.error("Video không tồn tại trong thư mục. Vui lòng kiểm tra lại.")
    
    # Thảo luận về các trường hợp lỗi trong các thách thức
    st.title("3. Thảo luận")
    
    st.write("""
    - **Background Clutters**: Nền có nhiều chuyển động hoặc đối tượng không liên quan có thể gây nhiễu cho thuật toán. 
        Để giảm thiểu vấn đề này, có thể áp dụng các kỹ thuật xử lý hình ảnh như loại bỏ nền hoặc tăng cường độ tương phản.
        
    - **Illumination Variations**: Sự thay đổi ánh sáng mạnh có thể ảnh hưởng đến độ chính xác của thuật toán. 
        Để cải thiện điều này, có thể sử dụng các phương pháp như cân bằng ánh sáng (brightness normalization) hoặc phát hiện biên (edge detection).
        
    - **Occlusion**: Khi đối tượng bị che khuất hoàn toàn, thuật toán có thể mất dấu đối tượng. 
        Để giải quyết vấn đề này, các phương pháp theo dõi kết hợp hoặc sử dụng deep learning có thể giúp nhận diện và theo dõi đối tượng trong điều kiện che khuất.
        
    - **Fast Motion**: Đối tượng di chuyển quá nhanh có thể khiến thuật toán không kịp cập nhật vị trí chính xác.
        Các giải pháp có thể bao gồm việc tăng tốc độ xử lý thuật toán hoặc sử dụng các tracker mạnh mẽ hơn có thể theo dõi đối tượng trong các điều kiện chuyển động nhanh.
    """)
if __name__ == "__main__":
    run_app9()
