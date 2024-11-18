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
    Bộ lọc được tối ưu hóa bằng cách sử dụng công thức sau:
    """)
    st.latex(r"""
        \hat{f} = \arg\min_f \sum_i \left\| \mathcal{K}(x_i, f) - y_i \right\|^2 + \lambda \|f\|^2
        """)
    st.markdown("""
    - $ \mathcal{K}(x_i, f) $ là sự tương quan giữa vị trí $ x_i $ trong hình ảnh và bộ lọc $ f $.
    - $ \mathcal{I}_i $ là các đặc trưng được trích xuất từ hình ảnh tại vị trí $ i $.
    - $ \lambda $ là tham số điều chỉnh độ phức tạp của bộ lọc và tránh overfitting.
    
    2. **Sử dụng kernel để tính toán đặc trưng (Kernel Computation):**
    Để tính toán đặc trưng giữa các điểm $ x $ và $ y $ trong không gian hình ảnh, ta sử dụng công thức:
    $$
    \mathcal{K}(x, y) = \phi(x)^\top \phi(y)
    $$
    Trong đó:
    - $ \phi(x) $ và $ \phi(y) $ là các hàm ánh xạ đặc trưng của điểm $ x $ và $ y $, giúp đưa các điểm trong không gian hình ảnh về một không gian đặc trưng có chiều cao hơn.
    
    3. **Tính toán vị trí đối tượng trong các frame kế tiếp:**
    Sau khi huấn luyện bộ lọc từ các frame trước, thuật toán sẽ tính toán vị trí của đối tượng trong frame tiếp theo bằng cách tìm điểm có giá trị cao nhất trong ma trận kết quả của phép tương quan giữa bộ lọc và các vùng trong hình ảnh.

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
    ### Các thách thức chính của thuật toán KCF
    
    1. **Nhiễu nền (Background Clutters):**
       - Khi nền chứa nhiều đối tượng chuyển động hoặc phức tạp, thuật toán dễ bị nhiễu.
       - Đối tượng có thể bị nhầm lẫn với các yếu tố không liên quan, đặc biệt trong môi trường đông đúc.
    
    2. **Thay đổi ánh sáng (Illumination Variations):**
       - Sự thay đổi mạnh về ánh sáng có thể làm biến dạng đặc trưng của đối tượng.
       - Giải pháp: Sử dụng các thuật toán xử lý trước như cân bằng sáng hoặc khử nhiễu.
    
    3. **Bị che khuất (Occlusion):**
       - Khi đối tượng bị các vật khác che khuất, KCF thường mất dấu hoặc theo dõi sai.
       - Đây là thách thức lớn, đặc biệt trong các video thực tế có nhiều vật cản.
    
    4. **Chuyển động nhanh (Fast Motion):**
       - Nếu đối tượng di chuyển quá nhanh giữa các khung hình, thuật toán không kịp cập nhật.
       - Điều này có thể dẫn đến sai lệch vị trí hoặc mất dấu đối tượng.
    
    ### Giải pháp tiềm năng:
    - **Cải thiện thuật toán:** Kết hợp KCF với các kỹ thuật hiện đại như Deep Learning hoặc Optical Flow.
    - **Tăng cường dữ liệu:** Sử dụng dữ liệu đa dạng với nhiều tình huống che khuất và thay đổi ánh sáng để huấn luyện mô hình tốt hơn.
    - **Xử lý trước:** Áp dụng các bước xử lý hình ảnh để làm nổi bật đặc trưng của đối tượng và giảm nhiễu từ nền.
    
    """)
        
    # Footer
    st.markdown("""
        **Lưu ý**: KCF có thể gặp khó khăn trong việc theo dõi khi đối tượng bị che khuất hoàn toàn, có sự thay đổi lớn về ánh sáng, hoặc di chuyển quá nhanh.
    """)
    
if __name__ == "__main__":
    run_app9()
