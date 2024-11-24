import streamlit as st

# Function to display the introduction section
def display_introduction():
    st.header("1. Giới thiệu")
    cols = st.columns([3, 1])

    with cols[1]:
        st.image(
            "services/sort_mot/benchmark-performance.jpg",
            use_column_width=True,
            caption=(
                "Đánh giá hiệu suất của SORT so với các thuật toán khác trong MOTChallenge 2015. "
                "(Nguồn: Simple Online and Realtime Tracking)."
            ),
        )

    with cols[0]:
        st.write(
            """
            - **SORT** là thuật toán theo dõi nhiều đối tượng **(Multi-Object Tracking - MOT)** nhanh, đơn giản, 
              được tối ưu cho thời gian thực.
            - Được giới thiệu vào năm 2016 qua bài báo [Simple Online and Realtime Tracking](https://arxiv.org/abs/1602.00763).
            - Biểu đồ bên phải minh họa hiệu suất SORT, cho thấy:
                - SORT có tốc độ cao trong khi vẫn đảm bảo độ chính xác.
                - Nhiều thuật toán khác có sự đánh đổi giữa tốc độ và độ chính xác.
            - **Hạn chế của SORT**:
                - Không duy trì ID khi đối tượng bị che khuất hoặc thoát khỏi khung hình.
                - Khó phân biệt các đối tượng tương tự về hình dạng, màu sắc.
                - Phụ thuộc vào mô hình detector để xác định vị trí đối tượng.
                - Không tối ưu khi đối tượng di chuyển nhanh hoặc không tuyến tính.
            """
        )

# Function to display the method section
def display_method():
    st.header("2. Phương pháp")
    st.write(
        """
        - **SORT** thuộc nhóm thuật toán **tracking-by-detection**, sử dụng mô hình detector như YOLO, Faster R-CNN,... 
          để xác định vị trí đối tượng và ghép nối các vị trí qua các khung hình liên tiếp.
        - Bốn bước hoạt động chính của SORT:
            1. **Phát hiện**: Xác định vị trí đối tượng trong frame bằng mô hình detector.
            2. **Dự đoán**: Vị trí tiếp theo của đối tượng với **Kalman Filter**.
            3. **Ghép nối**: Dùng thuật toán **Hungarian** để nối vị trí phát hiện và dự đoán.
            4. **Cập nhật**: Trạng thái đối tượng dựa trên kết quả ghép nối.
        """
    )

    st.columns([1, 8, 1])[1].image(
        "services/sort_mot/overview-SORT.png",
        use_column_width=True,
        caption="Minh họa hoạt động của SORT (Nguồn: Improved sheep identification and tracking algorithm based on YOLOv5 + SORT methods).",
    )

    st.subheader("2.1. Dự đoán vị trí bằng Kalman Filter")
    st.write(
        """
        - Mô hình dịch chuyển tuyến tính, với trạng thái đối tượng:
            $x = [u, v, s, r, \dot{u}, \dot{v}, \dot{s}]^T$, gồm:
            - $(u, v)$: Tọa độ trung tâm bounding box.
            - $s, r$: Tỷ lệ kích thước bounding box.
            - $(\dot{u}, \dot{v}, \dot{s})$: Vận tốc tương ứng.
        - Dự đoán vị trí tiếp theo bằng **Kalman Filter** dựa trên trạng thái hiện tại.
        """
    )

    st.subheader("2.2. Ghép nối bằng thuật toán Hungarian")
    st.write(
        """
        - Dựa trên ma trận chi phí $C$ (phần tử là IoU giữa các bounding box).
        - Áp dụng thuật toán [**Hungarian**](https://web.eecs.umich.edu/~pettie/matching/Kuhn-hungarian-assignment.pdf) 
          để tìm ghép nối tối ưu, tối đa hóa IoU.
        """
    )

    st.subheader("2.3. Cập nhật trạng thái")
    st.write(
        """
        - Các đối tượng được ghép nối sẽ cập nhật trạng thái.
        - Đối tượng không ghép nối sẽ được gán ID mới.
        - Đối tượng mất kết nối trong $T_{Lost}$ khung hình sẽ bị xóa. (Mặc định $T_{Lost} = 1$).
        """
    )

def display_visualization():
    st.header("3. Minh họa thuật toán")
    st.write(
        "- Dưới đây là video minh họa kết quả theo dõi đối tượng bằng thuật toán **SORT** kết hợp với mô hình phát hiện người đi bộ **YOLO**:"
    )
    st.video("services/sort_mot/YOLO_people_detection_SORT_tracking.mp4")
    st.write(
        """
        - Trong video, bạn có thể quan sát các ID được gán cho từng đối tượng trong khung hình.  
        - Một hạn chế dễ nhận thấy của **SORT** là khả năng duy trì ID không ổn định trong trường hợp đối tượng bị che khuất hoặc tạm thời thoát khỏi khung hình.  
        Ví dụ:  
        - Khi một người bị che khuất bởi vật cản hoặc tạm biến mất khỏi khung hình, ID ban đầu của họ có thể bị thay thế bởi một ID mới khi họ quay trở lại.
        """
    )


# Main application
def main():
    st.title("Giới thiệu và Phân tích SORT")
    display_introduction()
    display_method()
    display_visualization()

if __name__ == "__main__":
    main()
