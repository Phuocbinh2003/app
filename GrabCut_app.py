import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import base64
import json
from grabcut_processor import GrabCutProcessor

def run_app1():
    st.title("Cắt nền bằng GrabCut")

    uploaded_file = st.sidebar.file_uploader("Chọn hình ảnh", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        grabcut_processor = GrabCutProcessor(image_np)

        img_width, img_height = image.size

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

                canvas.addEventListener('mousedown', (event) => {{
                    if (event.button === 0 && !hasDrawnRectangle) {{
                        drawing = true;
                        startX = event.offsetX;
                        startY = event.offsetY;
                    }}
                    event.preventDefault();
                }});

                canvas.addEventListener('mouseup', (event) => {{
                    if (drawing) {{
                        drawing = false;
                        const endX = event.offsetX;
                        const endY = event.offsetY;

                        const rectX = Math.min(startX, endX);
                        const rectY = Math.min(startY, endY);
                        const rectWidth = Math.abs(startX - endX);
                        const rectHeight = Math.abs(startY - endY);

                        const x = Math.max(0, Math.min(rectX, canvas.width - 1));
                        const y = Math.max(0, Math.min(rectY, canvas.height - 1));
                        const width = Math.min(rectWidth, canvas.width - x);
                        const height = Math.min(rectHeight, canvas.height - y);

                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.rect(x, y, width, height);
                        ctx.strokeStyle = 'blue';
                        ctx.lineWidth = 2;
                        ctx.stroke();

                        const rect = {{ x: x, y: y, width: width, height: height }};
                        hasDrawnRectangle = true;
                        // Gửi dữ liệu hình chữ nhật về Streamlit
                        window.parent.postMessage(JSON.stringify({{ type: 'rect_data', rect }}), '*');
                        console.log("Rectangle data sent:", rect); // Ghi thông tin hình chữ nhật ra console
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

        # Nhận thông điệp từ JavaScript
        if st.session_state.get("rect_data"):
            rect_data = st.session_state.rect_data
            x = int(rect_data["x"])
            y = int(rect_data["y"])
            width = int(rect_data["width"])
            height = int(rect_data["height"])
            grabcut_processor.rect = (x, y, width, height)

        # Xử lý sự kiện từ JavaScript
        if "rect_data" in st.session_state:
            # Kiểm tra xem có dữ liệu hình chữ nhật không
            rect_data = st.session_state.rect_data
            if rect_data:
                st.success(f"Dữ liệu hình chữ nhật: {rect_data}")  # Hiển thị dữ liệu hình chữ nhật trên Streamlit
                grabcut_processor.rect = (rect_data["x"], rect_data["y"], rect_data["width"], rect_data["height"])

        # Hiển thị nút để áp dụng GrabCut
        if st.button("Áp dụng GrabCut"):
            if st.session_state.get("rect_data"):
                grabcut_processor.apply_grabcut()
                output_image = grabcut_processor.get_output_image()
                st.image(output_image, caption="Hình ảnh đầu ra", use_column_width=True)
            else:
                st.warning("Vui lòng vẽ một hình chữ nhật trước khi áp dụng GrabCut.")

        # Hướng dẫn sử dụng
        st.markdown("""## Hướng dẫn sử dụng
        1. Tải lên một hình ảnh bằng cách sử dụng menu ở bên trái.
        2. Nhấn chuột trái để vẽ hình chữ nhật quanh đối tượng bạn muốn cắt.
        3. Nhấn nút "Áp dụng GrabCut" để cắt nền.
        """)

# Hàm để mã hóa hình ảnh thành base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Bước 8: Chạy ứng dụng
if __name__ == "__main__":
    if 'rect_data' not in st.session_state:
        st.session_state.rect_data = None

    run_app1()
