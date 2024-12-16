import streamlit as st
from PIL import Image

# Function to display the introduction secti
def display_introduction():
    st.header("1. Giới thiệu")
    st.write(
        """
        **SORT (Simple Online and Realtime Tracking)** là một thuật toán theo dõi nhiều đối tượng (Multi-Object Tracking - MOT) 
        nhanh chóng, đơn giản và được tối ưu hóa cho thời gian thực. SORT thường được sử dụng trong các ứng dụng như giám sát, 
        phân tích video, và theo dõi đối tượng trong các hệ thống AI.
        
        SORT lần đầu tiên được giới thiệu qua bài báo 
        [Simple Online and Realtime Tracking (2016)](https://arxiv.org/abs/1602.00763). 
        Thuật toán này được thiết kế để cân bằng giữa tốc độ xử lý và độ chính xác trong môi trường thực tế.
        """
    )
    cols = st.columns([2, 1])

    with cols[0]:
        st.write(
            """
            ### Ưu điểm của SORT:
            - **Tốc độ cao**: SORT có thể hoạt động trong thời gian thực ngay cả trên các thiết bị phần cứng thông thường.
            - **Dễ triển khai**: Kết hợp đơn giản với các mô hình phát hiện (detector) hiện có như YOLO, Faster R-CNN.
            - **Độ chính xác hợp lý**: Mặc dù tốc độ cao, SORT vẫn duy trì hiệu suất đủ tốt trong nhiều trường hợp thực tế.

            ### Hạn chế của SORT:
            - **Duy trì ID không ổn định**: Khi đối tượng bị che khuất hoặc thoát khỏi khung hình, ID của nó có thể bị thay đổi.
            - **Phụ thuộc vào detector**: Nếu mô hình phát hiện không tốt, hiệu suất của SORT cũng bị ảnh hưởng.
            - **Không phù hợp với chuyển động phức tạp**: SORT không hoạt động tốt trong các tình huống đối tượng di chuyển phi tuyến tính hoặc thay đổi hình dạng nhanh.
            """
        )

    with cols[1]:
        st.image(
            "mot_sort/sort.png",
            use_column_width=True,
            caption="Hiệu suất của SORT so với các thuật toán khác (Nguồn: Simple Online and Realtime Tracking)."
        )

# Function to display the method section
def display_method():
    
   st.header("2. Phương pháp hoạt động")

    # Đưa ảnh minh họa cho phương pháp
    img = Image.open('mot_sort/buoc_sort.png')
    st.image(img, caption="", use_column_width=True)
    
    # Giới thiệu tổng quan về SORT
    st.write(
        """
        Thuật toán SORT (Simple Online and Realtime Tracking) là một thuật toán theo dõi đối tượng dựa trên phát hiện. Nó thuộc nhóm thuật toán **tracking-by-detection**, có nghĩa là thuật toán này sẽ sử dụng các **bounding box** (hộp giới hạn) mà một mô hình phát hiện đối tượng (như YOLOv5) cung cấp để theo dõi đối tượng qua các khung hình liên tiếp trong video. SORT sử dụng **Bộ lọc Kalman (Kalman Filter)** để dự đoán và cập nhật vị trí của các đối tượng trong mỗi khung hình.
        
        Các bước hoạt động chính của SORT bao gồm:
        """
    )
    
    st.markdown(
        """
        1. **Input**:
           - **Ảnh đầu vào**: Các khung hình liên tiếp từ video hoặc từ các camera.
           - **Object Detection**: Các mô hình phát hiện đối tượng như **YOLOv5** sẽ nhận diện và cung cấp các **bounding box** cho các đối tượng trong từng khung hình.
    
        2. **Data Association**:
           - **Cost Matrix Matching**: Tạo ma trận chi phí để khớp các đo lường mới (bounding box) với các đối tượng đã theo dõi trong các khung hình trước.
           - **Matched Measurement**: Các đo lường (bounding box) khớp với các đối tượng đã theo dõi sẽ được cập nhật trạng thái.
           - **Unmatched Measurement**: Những đối tượng mới không có bản ghi sẽ được tạo thành track mới.
           - **Unmatched Tracks**: Các đối tượng đã theo dõi nhưng không xuất hiện trong khung hình hiện tại sẽ bị tạm thời mất dấu.
    
        3. **Kalman Filter Estimation (KF Estimation)**:
           - **Kalman Filter Prediction**: Dự đoán trạng thái mới (ví trí, vận tốc) của đối tượng dựa trên trạng thái của nó trong các khung hình trước.
           - **Kalman Filter Update**: Cập nhật lại trạng thái dựa trên dữ liệu đo lường mới từ hệ thống phát hiện.
    
        4. **Track Management**:
           - **Track Initialization**: Khởi tạo track mới cho các đối tượng chưa được theo dõi.
           - **Deletion Conditions**: Xóa các track không tìm thấy đối tượng trong một số khung hình liên tiếp.
           - **Track Delete**: Quản lý việc xóa các track không còn hợp lệ sau khi không phát hiện đối tượng trong một số khung hình.
    
        5. **Output**:
           - **Bounding Boxes và Track IDs**: Các kết quả đầu ra bao gồm các **Bounding Boxes** (vị trí các đối tượng) và **Track IDs** (mã định danh duy nhất cho từng đối tượng qua các khung hình).
        """
    )
    
    # Input section
    st.subheader("1. Input")
    st.write(
        """
        Bước đầu tiên của thuật toán là nhận đầu vào từ các khung hình video hoặc hình ảnh.
        - **Ảnh đầu vào**: Là các khung hình từ video, trong đó mỗi khung hình chứa các đối tượng cần theo dõi.
        - **Object Detection**: Mô hình phát hiện đối tượng như **YOLOv5** hoặc các mô hình tương tự được sử dụng để nhận diện và phát hiện các đối tượng trong mỗi khung hình. Mỗi đối tượng được phát hiện sẽ có một **bounding box** (hộp giới hạn) bao quanh.
        """
    )
    
    # Data Association Section
    st.subheader("2. Data Association")
    st.write(
        """
        Bước Data Association là bước quan trọng để xác định mối quan hệ giữa các đo lường mới (bounding boxes) và các track đã có. Mục tiêu là đảm bảo rằng mỗi bounding box phát hiện mới sẽ được gán đúng đối tượng đang được theo dõi, và nếu không tìm thấy sự phù hợp, track mới sẽ được khởi tạo.
        
        - **Cost Matrix Matching**: Trong bước này, thuật toán tạo ra một **ma trận chi phí** (cost matrix), trong đó mỗi phần tử đại diện cho chi phí gán một bounding box mới với một track hiện có. Chi phí này có thể được tính toán dựa trên khoảng cách Euclidean giữa vị trí của bounding box và dự đoán vị trí của track.
        
        - **Matched Measurement**: Các bounding box mới sẽ được gán cho các track hiện có nếu chúng có chi phí thấp nhất trong ma trận chi phí. Các đối tượng này sẽ được cập nhật trạng thái mới.
        
        - **Unmatched Measurement**: Các bounding box không khớp với bất kỳ track nào hiện có sẽ được xem là đối tượng mới và khởi tạo track mới cho chúng.
        
        - **Unmatched Tracks**: Các track đã tồn tại nhưng không khớp với bất kỳ bounding box nào trong khung hình hiện tại sẽ bị tạm thời "mất dấu". Những track này có thể bị xóa sau một số khung hình nếu không được phát hiện lại.
        """
    )
    
    # Kalman Filter Section
    st.subheader("3. Kalman Filter Estimation")
    st.write(
        """
        Bộ lọc Kalman (Kalman Filter) là thành phần quan trọng giúp dự đoán và cập nhật trạng thái của các đối tượng. Bộ lọc Kalman hoạt động dựa trên việc kết hợp giữa thông tin dự đoán từ trạng thái trước đó và các đo lường mới từ hệ thống phát hiện đối tượng.
        
        - **Prediction**: Dự đoán trạng thái của đối tượng trong khung hình tiếp theo. Dự đoán này được thực hiện dựa trên trạng thái và vận tốc của đối tượng trong các khung hình trước.
        
        - **Update**: Khi có thông tin mới từ hệ thống phát hiện đối tượng, bộ lọc Kalman sẽ cập nhật lại trạng thái của đối tượng để phản ánh các thay đổi từ môi trường bên ngoài.
        """
    )
    st.markdown(
        """
        > **Công thức Prediction**:
        > \\[
        x_{k|k-1} = F x_{k-1} + B u_k, \quad P_{k|k-1} = F P_{k-1} F^T + Q
        \\]
        > **Công thức Update**:
        > \\[
        K_k = P_{k|k-1} H^T (H P_{k|k-1} H^T + R)^{-1}, \quad x_k = x_{k|k-1} + K_k (z_k - H x_{k|k-1})
        \\]
        """
    )
    
    # Track Management Section
    st.subheader("4. Track Management")
    st.write(
        """
        Quản lý track là một bước quan trọng giúp duy trì sự liên tục của quá trình theo dõi. Các track phải được khởi tạo khi phát hiện đối tượng mới và phải bị xóa nếu không còn được phát hiện trong một số khung hình liên tiếp.
        
        - **Track Initialization**: Track mới được khởi tạo khi một đối tượng chưa có bản ghi trong hệ thống theo dõi. Đối tượng này sẽ bắt đầu một track mới.
        
        - **Deletion Conditions**: Các track sẽ bị xóa nếu không có bất kỳ bounding box nào khớp với track đó trong một số lượng khung hình liên tiếp.
        
        - **Track Delete**: Các track bị mất dấu sau nhiều khung hình sẽ được xóa khỏi hệ thống để giảm tải.
        """
    )
    
    # Output Section
    st.subheader("5. Output")
    st.write(
        """
        Kết quả đầu ra của thuật toán SORT bao gồm:
        - **Bounding Boxes**: Vị trí của các đối tượng trong mỗi khung hình được xác định bởi các bounding box. Mỗi bounding box đại diện cho phạm vi không gian của đối tượng trong ảnh.
        - **Track IDs**: Mỗi đối tượng theo dõi sẽ được gán một ID duy nhất để giúp phân biệt và theo dõi đối tượng đó qua nhiều khung hình liên tiếp.
        """
    )
    
    st.success("Quá trình này đảm bảo theo dõi các đối tượng một cách chính xác và hiệu quả trong thời gian thực.")

# Function to display the visualization section
def display_visualization():
    st.header("3. Minh họa thuật toán SORT")
    st.write(
        """
        Dưới đây là video minh họa cách SORT kết hợp với YOLO để theo dõi đối tượng (ví dụ: người đi bộ) trong một video.  
        Video cho thấy ID của từng đối tượng trong khung hình và khả năng theo dõi đối tượng khi chúng di chuyển.
        """
    )
    st.video("mot_sort/video.mp4")
    st.write(
        """
        ### Quan sát từ video:
        - SORT duy trì ID khá tốt khi đối tượng di chuyển thông thường.  
        - Khi đối tượng bị che khuất hoặc tạm thời rời khỏi khung hình, ID của nó có thể bị thay thế bởi ID mới khi nó quay trở lại(giây 12).  
        Đây là một trong những hạn chế lớn của thuật toán SORT.
        """
    )

# Main application
def run_app10():
    st.title("Giới thiệu và Phân tích SORT")
    display_introduction()
    st.markdown("---")
    display_method()
    st.markdown("---")
    display_visualization()
    st.markdown("---")
    st.info("**Tài liệu tham khảo**: [Simple Online and Realtime Tracking](https://arxiv.org/abs/1602.00763)")

if __name__ == "__main__":
    run_app10()
