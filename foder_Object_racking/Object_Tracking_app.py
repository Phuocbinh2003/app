import streamlit as st
import cv2
import os



def run_app9():
    # Tiêu đề của ứng dụn
    st.title("1. Object Tracking Using KCF")
    
    st.markdown("""
    **KCF (Kernelized Correlation Filters)** là một thuật toán mạnh mẽ trong việc theo dõi đối tượng. 
    KCF sử dụng kỹ thuật kernel để cải thiện hiệu suất và độ chính xác, đặc biệt trong các tình huống có sự thay đổi trong đối tượng và nền.
    
    Thuật toán này sử dụng **kernel trick** để làm việc với không gian hình ảnh phức tạp mà không cần thay đổi dữ liệu ban đầu. 
    Mục tiêu là phát hiện đối tượng trong mỗi frame của video và theo dõi sự thay đổi vị trí của nó theo thời gian.

    ### Công thức của KCF:

    1. **Cập nhật bộ lọc (Filter Update):**
    \[
    \hat{f}(x) = \text{argmin}_f \sum_i || \mathcal{K}(x_i, f) - \mathcal{I}_i ||^2 + \lambda ||f||^2
    \]
    Trong đó:
    - \( \mathcal{K}(x_i, f) \) là sự tương quan giữa vị trí \( x_i \) trong hình ảnh và bộ lọc \( f \).
    - \( \mathcal{I}_i \) là các đặc trưng được trích xuất từ hình ảnh.
    - \( \lambda \) là tham số điều chỉnh độ phức tạp của bộ lọc.

    2. **Sử dụng kernel để tính toán đặc trưng:**
    \[
    \mathcal{K}(x, y) = \phi(x)^\top \phi(y)
    \]
    Trong đó:
    - \( \phi(x) \) và \( \phi(y) \) là các hàm ánh xạ đặc trưng của điểm \( x \) và \( y \).

    3. **Tính toán vị trí đối tượng trong các frame kế tiếp:**
    Khi bộ lọc đã được huấn luyện từ các frame trước đó, thuật toán sẽ tính toán vị trí của đối tượng trong frame tiếp theo bằng cách tìm điểm có giá trị cao nhất trong ma trận kết quả của phép tương quan.

    Thuật toán này mang lại hiệu suất tốt trong nhiều tình huống với các đối tượng di chuyển chậm hoặc thay đổi hình dạng không quá lớn.
    """)
    
    # Ví dụ minh họa
    st.title("2. Ví dụ minh họa")
    
    # Đường dẫn video có sẵn trong thư mục
    video_path = "foder_Object_racking/Untitled video - Made with Clipchamp.mp4"  # Thay thế 'your_video.mp4' bằng tên video của bạn trong thư mục 'videos'
    
    # Kiểm tra xem video có tồn tại hay không
    if os.path.exists(video_path):
        # Hiển thị video từ thư mục
        st.video(video_path)
    else:
        st.error("Video không tồn tại trong thư mục. Vui lòng kiểm tra lại.")
    
    # Thảo luận về các trường hợp lỗi trong các thách thức
    st.title("3. Thảo luận")
    
    st.write("""
        Dưới đây là một số thách thức mà thuật toán KCF có thể gặp phải trong quá trình theo dõi đối tượng:
    
        - **Background Clutters**: Khi nền chứa nhiều chuyển động hoặc đối tượng không liên quan, thuật toán có thể bị nhiễu và không nhận diện đúng đối tượng. KCF cần cải thiện khả năng phân biệt giữa đối tượng và các yếu tố nền.
    
        - **Illumination Variations**: Sự thay đổi ánh sáng mạnh trong video có thể làm thay đổi hình dạng và đặc trưng của đối tượng, làm cho việc theo dõi gặp khó khăn. Để khắc phục, cần có các phương pháp xử lý ánh sáng hoặc sử dụng các thuật toán khử nhiễu.
    
        - **Occlusion**: Khi đối tượng bị che khuất bởi các đối tượng khác, KCF có thể mất dấu và không thể theo dõi chính xác. Đây là một trong những thách thức lớn nhất trong việc theo dõi đối tượng thực tế.
    
        - **Fast Motion**: Nếu đối tượng di chuyển quá nhanh, thuật toán có thể không kịp cập nhật vị trí chính xác. Điều này có thể dẫn đến việc mất dấu đối tượng hoặc theo dõi sai vị trí.
    """)
    
    # Footer
    st.markdown("""
        **Lưu ý**: KCF có thể gặp khó khăn trong việc theo dõi khi đối tượng bị che khuất hoàn toàn, có sự thay đổi lớn về ánh sáng, hoặc di chuyển quá nhanh.
    """)
if __name__ == "__main__":
    run_app9()
