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


    # Header Section
    st.header("2. Phương pháp hoạt động")
    img = Image.open('mot_sort/buoc_sort.png')
    st.image(img, caption="Sơ đồ thuật toán SORT", use_column_width=True)

    # Introduction
    st.write(
        """
        SORT thuộc nhóm thuật toán **tracking-by-detection**, nghĩa là nó dựa vào các bounding box do mô hình phát hiện 
        cung cấp để theo dõi đối tượng qua các khung hình. Thuật toán gồm các bước chính sau đây:
        """
    )

    # Step 1: Object Detection
    st.subheader("Bước 1: Phát hiện đối tượng (Detection)")
    st.write(
        """
        - Sử dụng các mô hình như YOLO, Faster R-CNN, SSD hoặc RetinaNet để phát hiện bounding box của các đối tượng trong từng khung hình.
        - Đầu ra là tập hợp các bounding box với tọa độ $(x, y, w, h)$ tương ứng, cùng với lớp đối tượng.
        - Ví dụ: Một khung hình chứa các đối tượng như người đi bộ, xe hơi hoặc xe đạp.
        """
    )

    # Step 2: Prediction
    st.subheader("Bước 2: Dự đoán vị trí tiếp theo (Prediction)")
    st.write(
        """
        - Áp dụng **Kalman Filter** để dự đoán vị trí tiếp theo của đối tượng dựa trên trạng thái hiện tại.
        - Trạng thái của đối tượng được biểu diễn dưới dạng vector:
        """
    )
    st.latex(r"""
    x = [u, v, s, r, \dot{u}, \dot{v}, \dot{s}]^T
    """
    )
    st.write(
        """
        Trong đó:
        - $(u, v)$: Tọa độ trung tâm của bounding box.  
        - $s$: Diện tích của bounding box.  
        - $r$: Tỷ lệ khung hình (width/height).  
        - $(\dot{u}, \dot{v}, \dot{s})$: Tốc độ thay đổi của các tham số tương ứng.  
        - Dựa trên trạng thái này, Kalman Filter dự đoán vị trí tiếp theo trước khi nhận dữ liệu từ khung hình mới.
        - Kalman Filter gồm hai bước chính:
            1. **Dự đoán (Prediction):** Dự đoán trạng thái mới dựa trên trạng thái trước đó.
            2. **Cập nhật (Update):** Điều chỉnh dự đoán bằng dữ liệu quan sát thực tế.
        """
    )

    # Step 3: Data Association
    st.subheader("Bước 3: Ghép nối đối tượng (Data Association)")
    st.write(
        """
        - Sử dụng **Hungarian Algorithm** để ghép nối bounding box dự đoán và phát hiện dựa trên ma trận chi phí $C$.
        - Ma trận chi phí $C$ được tính dựa trên độ tương đồng IoU (Intersection over Union):
        """
    )
    st.latex(r"""
    C_{ij} = 1 - \text{IoU}(B_i, B_j)
    """
    )
    st.write(
        """
        Trong đó:
        - $C_{ij}$: Chi phí giữa bounding box $B_i$ (dự đoán) và $B_j$ (phát hiện).
        - $\text{IoU}$: Tỉ lệ giao nhau trên hợp giữa hai bounding box.
        - **Hungarian Algorithm:** Giải bài toán tối ưu ghép nối sao cho tổng chi phí là nhỏ nhất. Kết quả ghép nối xác định bounding box nào thuộc về đối tượng nào qua các khung hình.
        - Các bounding box không được ghép nối có thể được gán ID mới hoặc bị loại bỏ.
        """
    )

    # Step 4: State Update
    st.subheader("Bước 4: Cập nhật trạng thái (State Update)")
    st.write(
        """
        - Đối tượng được ghép nối sẽ cập nhật trạng thái dựa trên kết quả mới từ Kalman Filter.
        - Đối tượng không ghép nối trong một số khung hình (thường là $T_{Lost} = 1$) sẽ bị xóa khỏi danh sách theo dõi.
        - Đối tượng mới xuất hiện trong khung hình sẽ được khởi tạo với ID mới.
        - Kết quả cuối cùng là tập hợp các bounding box và ID tương ứng với mỗi đối tượng.
        """
    )

    # Summary
    st.subheader("Tóm tắt quy trình")
    st.write(
        """
        1. Phát hiện đối tượng trong khung hình hiện tại bằng mô hình phát hiện như YOLO hoặc Faster R-CNN.
        2. Sử dụng Kalman Filter để dự đoán trạng thái của các đối tượng đã theo dõi.
        3. Ghép nối các dự đoán với kết quả phát hiện qua Hungarian Algorithm.
        4. Cập nhật trạng thái hoặc khởi tạo đối tượng mới.
        5. Trả về danh sách các bounding box và ID đối tượng.
        
        **Ví dụ ứng dụng:**
        - Theo dõi xe cộ trên đường trong video giám sát giao thông.
        - Theo dõi người trong hệ thống camera an ninh.
        """
    )


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
