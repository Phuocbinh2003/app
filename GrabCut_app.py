import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import base64
from grabcut_processor import GrabCutProcessor

# Hàm xử lý tin nhắn từ JavaScript (với postMessage)
def handle_js_messages():
    message = st.experimental_get_query_params()
    st.write("Received message:", message)  # Kiểm tra tin nhắn nhận từ JavaScript
    if "rect_data" in message:
        rect_data_str = message["rect_data"][0]  # Nhận chuỗi JSON từ query param
        st.write("Raw rect_data string:", rect_data_str)  # Hiển thị chuỗi raw
        try:
            rect_data = eval(rect_data_str)  # Chuyển chuỗi JSON thành dict
            st.session_state.rect_data = rect_data  # Lưu vào session_state
            st.write("Updated rect_data in session state:", st.session_state.rect_data)  # Kiểm tra giá trị lưu vào session_state
        except Exception as e:
            st.error(f"Lỗi khi xử lý rect_data: {e}")

# Hàm chính chạy ứng dụng
def run_app1():
    st.title("Cắt nền bằng GrabCut")

    # Thanh bên để tải lên hình ảnh
    uploaded_file = st.sidebar.file_uploader("Chọn hình ảnh", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Đọc hình ảnh
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        # Khởi tạo bộ xử lý GrabCut
        grabcut_processor = GrabCutProcessor(image_np)

        # Lấy kích thước của hình ảnh
        img_width, img_height = image.size

        # HTML và CSS cho việc vẽ hình chữ nhật
        drawing_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column; 
                    align-items: center; 
                }}
                .canvas-container {{
                    position: relative; 
                    border: 1px solid black; 
                    width: {img_width}px; 
                    height: {img_height}px; 
                }}
                canvas {{
                    cursor: crosshair;
                    position: absolute; 
                    top: 0;
                    left: 0;
                    width: {img_width}px; 
                    height: {img_height}px; 
                    display: block; 
                    z-index: 1; 
                }}
                img {{
                    width: {img_width}px; 
                    height: {img_height}px; 
                    position: absolute; 
                    top: 0;
                    left: 0;
                    z-index: 0; 
                }}
            </style>
        </head>
        <body>
            <div class="canvas-container">
                <img id="originalImage" src="data:image/png;base64,{convert_image_to_base64(image)}" />
                <canvas id="drawingCanvas" width="{img_width}" height="{img_height}"></canvas>
            </div>
            <script>
                const canvas = document.getElementById('drawingCanvas');
                const ctx = canvas.getContext('2d');
                const img = document.getElementById('originalImage');

                let drawing = false;
                let startX, startY;
                let hasDrawnRectangle = false; 

                // Bắt đầu vẽ hình chữ nhật khi nhấn chuột
                canvas.addEventListener('mousedown', (event) => {{
                    if (event.button === 0 && !hasDrawnRectangle) {{
                        drawing = true;
                        startX = event.offsetX;
                        startY = event.offsetY;
                    }}
                    event.preventDefault();
                }});

                // Kết thúc vẽ hình chữ nhật khi thả chuột
                canvas.addEventListener('mouseup', (event) => {{
                    if (drawing) {{
                        drawing = false;
                        const endX = event.offsetX;
                        const endY = event.offsetY;
                        const width = endX - startX;
                        const height = endY - startY;

                        ctx.clearRect(0, 0, canvas.width, canvas.height); 
                        ctx.rect(startX, startY, width, height); 
                        ctx.strokeStyle = 'blue';
                        ctx.lineWidth = 2;
                        ctx.stroke();

                        const rect = {{ x: startX, y: startY, width: width, height: height }};
                        hasDrawnRectangle = true;

                        // Gửi thông điệp tới Streamlit
                        window.parent.postMessage(JSON.stringify({{ type: 'rect_data', rect }}), '*');
                    }}
                }});

                canvas.addEventListener('mousemove', (event) => {{
                    if (drawing) {{
                        event.preventDefault();
                    }}
                }});
            </script>
        </body>
        </html>
        """

        # Hiển thị canvas và hình ảnh
        st.components.v1.html(drawing_html, height=img_height + 50)

        # Khởi tạo khóa rect_data trong session_state nếu chưa tồn tại
        if 'rect_data' not in st.session_state:
            st.session_state.rect_data = None

        # Nhận thông điệp từ JavaScript và cập nhật session_state
        handle_js_messages()

        # Xử lý dữ liệu hình chữ nhật từ JavaScript
        if st.session_state["rect_data"] is not None:
            st.write("rect_data exists:", st.session_state["rect_data"])  # Kiểm tra dữ liệu có tồn tại
            rect_data = st.session_state["rect_data"]
            x = int(rect_data["x"])
            y = int(rect_data["y"])
            width = int(rect_data["width"])
            height = int(rect_data["height"])
            grabcut_processor.rect = (x, y, width, height)

            # Hiển thị thông tin về hình chữ nhật
            st.write(f"Tọa độ hình chữ nhật: (x: {x}, y: {y}), kích thước: {width}x{height}")
        else:
            st.write("rect_data is None")  # Thông báo nếu không có dữ liệu

        # Hiển thị nút để áp dụng GrabCut
        if st.button("Áp dụng GrabCut"):
            if st.session_state.rect_data:
                grabcut_processor.apply_grabcut()
                output_image = grabcut_processor.get_output_image()
                st.image(output_image, caption="Hình ảnh đầu ra", use_column_width=True)
            else:
                st.warning("Vui lòng vẽ một hình chữ nhật trước khi áp dụng GrabCut.")

        # Hướng dẫn sử dụng
        st.markdown("""
        ## Hướng dẫn sử dụng
        1. Tải lên một hình ảnh bằng cách sử dụng menu ở bên trái.
        2. Nhấn chuột trái để vẽ hình chữ nhật quanh đối tượng bạn muốn cắt.
        3. Nhấn nút "Áp dụng GrabCut" để cắt nền.
        """)

# Hàm để mã hóa hình ảnh thành base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Chạy ứng dụng
if __name__ == "__main__":
    if 'rect_data' not in st.session_state:
        st.session_state.rect_data = None

    run_app1()
