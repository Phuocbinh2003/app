import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import base64
import json
from grabcut_processor import GrabCutProcessor

def run_app1():
    st.title("Cắt nền bằng GrabCut")

    # Sidebar for image upload
    uploaded_file = st.sidebar.file_uploader("Chọn hình ảnh", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        # Display the original image
        st.image(image, caption="Hình ảnh gốc", use_column_width=True)

        # Initialize GrabCut processor
        grabcut_processor = GrabCutProcessor(image_np)

        # HTML and CSS for drawing
        drawing_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;  /* Xóa margin của body */
                    padding: 0; /* Xóa padding của body */
                }}
                canvas {{
                    border: 1px solid black;
                    cursor: crosshair;
                    display: block; /* Đảm bảo canvas không có khoảng trắng */
                }}
            </style>
        </head>
        <body>
            <canvas id="drawingCanvas" width="{image.width}" height="{image.height}"></canvas>
            <script>
                const canvas = document.getElementById('drawingCanvas');
                const ctx = canvas.getContext('2d');
                const img = new Image();
                img.src = '{convert_image_to_base64(image)}';

                img.onload = function() {{
                    ctx.drawImage(img, 0, 0);
                }};

                let drawing = false;
                let startX, startY;

                canvas.addEventListener('mousedown', (event) => {{
                    if (event.button === 0) {{ // Nút chuột trái
                        drawing = true;
                        startX = event.offsetX;
                        startY = event.offsetY;
                    }}
                    event.preventDefault(); // Ngăn chặn hành vi kéo ảnh
                }});

                canvas.addEventListener('mouseup', (event) => {{
                    if (drawing) {{
                        drawing = false;
                        const endX = event.offsetX;
                        const endY = event.offsetY;
                        const width = Math.abs(startX - endX);
                        const height = Math.abs(startY - endY);

                        ctx.rect(startX, startY, width, height);
                        ctx.strokeStyle = 'blue';
                        ctx.lineWidth = 2;
                        ctx.stroke();

                        const rect = {{ x: Math.min(startX, endX), y: Math.min(startY, endY), width: width, height: height }};
                        window.parent.postMessage(JSON.stringify(rect), '*');
                    }}
                }});

                // Ngăn chặn hành vi kéo chuột khi di chuyển
                canvas.addEventListener('mousemove', (event) => {{
                    if (drawing) {{
                        event.preventDefault();
                    }}
                }});
            </script>
        </body>
        </html>
        """

        # Display the canvas
        st.components.v1.html(drawing_html, height=image.height)

        # Button to apply GrabCut
        if st.button("Áp dụng GrabCut"):
            # Get rectangle coordinates from JavaScript message
            if st.session_state.get("rect_data", None) is not None:
                rect_data = st.session_state.rect_data
                x = int(rect_data["x"])
                y = int(rect_data["y"])
                width = int(rect_data["width"])
                height = int(rect_data["height"])
                grabcut_processor.rect = (x, y, width, height)
                grabcut_processor.apply_grabcut()
                output_image = grabcut_processor.get_output_image()
                st.image(output_image, caption="Hình ảnh đầu ra", use_column_width=True)

        # Instructions
        st.markdown("""
        ## Hướng dẫn sử dụng
        1. Tải lên một hình ảnh bằng cách sử dụng menu ở bên trái.
        2. Nhấn chuột trái để vẽ hình chữ nhật quanh đối tượng bạn muốn cắt.
        3. Nhấn nút "Áp dụng GrabCut" để cắt nền.
        """)

# Function to encode image to base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Bước 8: Chạy ứng dụng
if __name__ == "__main__":
    run_app1()
