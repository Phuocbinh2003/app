import streamlit as st

# Function to display the introduction sectio
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
    st.write(
        """
        SORT thuộc nhóm thuật toán **tracking-by-detection**, nghĩa là nó dựa vào các bounding box do mô hình phát hiện 
        cung cấp để theo dõi đối tượng qua các khung hình. Các bước hoạt động chính của SORT gồm:
        """
    )
    st.markdown(
        """
        1. **Phát hiện đối tượng (Detection)**:
           - Sử dụng các mô hình như YOLO, Faster R-CNN để phát hiện bounding box của các đối tượng trong từng khung hình.
        2. **Dự đoán vị trí tiếp theo (Prediction)**:
           - Áp dụng **Kalman Filter** để dự đoán vị trí tiếp theo của đối tượng dựa trên trạng thái hiện tại.
        3. **Ghép nối đối tượng (Assignment)**:
           - Sử dụng **Hungarian Algorithm** để ghép nối các bounding box dự đoán và phát hiện dựa trên độ tương đồng (IoU).
        4. **Cập nhật trạng thái (Update)**:
           - Cập nhật trạng thái đối tượng (vị trí, vận tốc,...) hoặc gán ID mới cho các đối tượng mới xuất hiện.
        """
    )

    st.subheader("2.1. Kalman Filter")
    st.write(
    """
    Kalman Filter là một thuật toán ước tính trạng thái của một hệ thống động lực tuyến tính. Trong SORT, trạng thái của đối tượng được biểu diễn dưới dạng:
    """
    )
    st.latex(r"""
    x = [u, v, s, r, \dot{u}, \dot{v}, \dot{s}]^T
    """)
    st.write(
        """
        - $(u, v)$: Tọa độ trung tâm bounding box.  
        - $s$: Diện tích bounding box.  
        - $r$: Tỷ lệ khung hình (width/height).  
        - $(\dot{u}, \dot{v}, \dot{s})$: Tốc độ thay đổi tương ứng.
    
        Kalman Filter dự đoán vị trí tiếp theo dựa trên trạng thái hiện tại và cập nhật khi có dữ liệu mới.
        """
    )


    st.subheader("2.2. Hungarian Algorithm")
    st.write(
        """
        Hungarian Algorithm là một thuật toán tối ưu để giải bài toán ghép nối. Trong SORT, nó được sử dụng để ghép nối 
        các bounding box dự đoán và bounding box phát hiện dựa trên ma trận chi phí $C$, với:
        \[
        C_{ij} = 1 - \text{IoU}(B_i, B_j)
        \]
        - $C_{ij}$: Chi phí giữa bounding box $B_i$ (dự đoán) và $B_j$ (phát hiện).  
        - $\text{IoU}$: Intersection over Union giữa hai bounding box.
        """
    )

    st.subheader("2.3. Cập nhật trạng thái")
    st.write(
        """
        - Đối tượng được ghép nối sẽ cập nhật trạng thái dựa trên kết quả mới.  
        - Đối tượng không ghép nối trong một số khung hình (mặc định $T_{Lost} = 1$) sẽ bị xóa.  
        - Đối tượng mới xuất hiện sẽ được gán ID mới.
        """
    )

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
        - Khi đối tượng bị che khuất hoặc tạm thời rời khỏi khung hình, ID của nó có thể bị thay thế bởi ID mới khi nó quay trở lại.  
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
