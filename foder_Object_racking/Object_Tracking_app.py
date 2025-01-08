import streamlit as st
import cv2
import os

def run_app9():
    # Tiêu đề của ứng dụn
    st.title("1. Object Tracking Using KCF")

    # Introduction
    st.markdown("""
    **KCF (Kernelized Correlation Filters)** là một thuật toán mạnh mẽ dùng để theo dõi đối tượng qua các khung hình video. 
    Thuật toán này tận dụng kỹ thuật **kernel trick** để hoạt động trong không gian đặc trưng cao, cho phép phát hiện chính xác vị trí của đối tượng.
    
    **Cách hoạt động:**
    - **Đầu vào:** Một video hoặc chuỗi khung hình, với một khung hình ban đầu chứa đối tượng được chọn thủ công hoặc tự động.
    - **Theo dõi:** KCF sẽ tính toán các vùng ảnh xung quanh vị trí đối tượng hiện tại, sau đó tìm kiếm vùng có sự tương đồng cao nhất để xác định vị trí mới của đối tượng.
    
    KCF hoạt động qua ba bước chính:
    """)
    
    # Step 1: Update Filter
    st.subheader("Bước 1: Cập nhật bộ lọc (Filter Update)")
    st.markdown("""
    KCF sử dụng một bộ lọc để dự đoán vị trí của đối tượng. Bộ lọc được tối ưu hóa bằng cách giải bài toán tối thiểu hóa:
    """)
    st.latex(r"""
    \hat{f} = \arg\min_f \sum_i \left\| \mathcal{K}(x_i, f) - y_i \right\|^2 + \lambda \|f\|^2
    """)
    st.markdown("""
    - **Ý nghĩa các tham số:**
      - $ \mathcal{K}(x_i, f) $: Giá trị tương quan giữa điểm ảnh $x_i$ và bộ lọc $f$.
      - $y_i$: Giá trị đầu ra mong muốn (thường là vị trí đối tượng trong không gian ảnh).
      - $\lambda$: Tham số điều chỉnh để tránh hiện tượng quá khớp (overfitting).
      - $f$: Bộ lọc tối ưu cần tìm.
    - Công thức trên tìm kiếm bộ lọc $f$ sao cho sai số giữa giá trị dự đoán và thực tế là nhỏ nhất.
    """)
    
    # Step 2: Kernel Computation
    st.subheader("Bước 2: Tính toán Kernel (Kernel Computation)")
    st.markdown("""
    KCF sử dụng **kernel trick** để chuyển các điểm từ không gian gốc sang không gian đặc trưng cao hơn, giúp tăng độ chính xác khi theo dõi. 
    Công thức tính kernel:
    """)
    st.latex(r"""
    \mathcal{K}(x, y) = \phi(x)^\top \phi(y)
    """)
    st.markdown("""
    - **Ý nghĩa các tham số:**
      - $\phi(x)$ và $\phi(y)$: Hàm ánh xạ đặc trưng của hai điểm $x$ và $y$.
      - $\mathcal{K}(x, y)$: Độ tương đồng giữa hai điểm trong không gian đặc trưng.
    - Một số kernel thường dùng:
      - **Kernel tuyến tính:** $\mathcal{K}(x, y) = x^\top y$
      - **Kernel Gaussian:** $\mathcal{K}(x, y) = \exp(-\|x - y\|^2 / \sigma^2)$
    """)
    
    # Step 3: Target Localization
    st.subheader("Bước 3: Xác định vị trí đối tượng (Target Localization)")
    st.markdown("""
    Sau khi huấn luyện bộ lọc, KCF sử dụng bộ lọc này để tìm vị trí của đối tượng trong khung hình tiếp theo. Quá trình này thực hiện bằng cách:
    1. Tính giá trị tương quan giữa bộ lọc và các vùng trong khung hình.
    2. Xác định vị trí có giá trị tương quan cao nhất, đây là vị trí của đối tượng.
    
    Công thức tính:
    """)
    st.latex(r"""
    \text{Response Map} = \mathcal{K}(x, f)
    """)
    st.markdown("""
    - **Ý nghĩa:**
      - $\mathcal{K}(x, f)$: Giá trị tương quan giữa mỗi vùng $x$ trong khung hình và bộ lọc $f$.
      - Vị trí có giá trị cao nhất trong bản đồ đáp ứng (Response Map) là vị trí của đối tượng.
    """)
    
    # Example: How KCF Works
    st.subheader("Ví dụ minh họa hoạt động của KCF")
    st.markdown("""
    1. **Đầu vào:** Một video, ví dụ như cảnh theo dõi bóng trong trận đấu.
       - Người dùng chọn một khung hình đầu tiên và đánh dấu vị trí của quả bóng.
    2. **Quá trình theo dõi:**
       - Ở mỗi khung hình, KCF tính toán giá trị tương quan giữa bộ lọc đã được cập nhật và các vùng ảnh xung quanh vị trí dự đoán.
       - Vùng có giá trị tương quan cao nhất được chọn làm vị trí mới của quả bóng.
    3. **Kết quả:** Một đường dẫn liên tục được tạo ra, biểu diễn vị trí quả bóng trong suốt chuỗi video.
    """)
    
    # Summary
    st.subheader("Tóm tắt")
    st.markdown("""
    KCF là thuật toán theo dõi đối tượng hiệu quả nhờ sử dụng kernel trick và tối ưu hóa bộ lọc. 
    Các bước chính:
    1. Huấn luyện bộ lọc để nhận diện đối tượng.
    2. Sử dụng kernel để xác định tương quan giữa đối tượng và các vùng ảnh.
    3. Xác định vị trí đối tượng trong các khung hình kế tiếp dựa trên giá trị tương quan.
    
    **Ứng dụng:**
    - Theo dõi khuôn mặt trong camera.
    - Theo dõi xe cộ trong giám sát giao thông.
    - Theo dõi bóng trong các trận đấu thể thao.
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
