import streamlit as st
import cv2 as cv
import numpy as np
import base64
import re
from grabcut_processor import GrabCutProcessor  # Nhập lớp GrabCutProcessor

def get_image_with_canvas(image):
    """Return HTML with canvas for drawing rectangles."""
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    height, width = image.shape[:2]

    html = f"""
    <div style="position: relative; padding-bottom: 30px;">
        <img id="image" src="data:image/png;base64,{img_base64}" style="width: {width}px; height: {height}px;"/>
        <canvas id="canvas" width="{width}" height="{height}" style="position: absolute; top: 0; left: 0; border: 1px solid red;"></canvas>
        <div id="rectInfo" style="margin-top: 10px; position: relative; z-index: 1;"></div>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = document.getElementById('image');
        const rectInfoDiv = document.getElementById('rectInfo');
        let startX, startY, isDrawing = false;

        canvas.addEventListener('mousedown', function(e) {{
            startX = e.offsetX;
            startY = e.offsetY;
            isDrawing = true;
        }});

        canvas.addEventListener('mousemove', function(e) {{
            if (isDrawing) {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                ctx.strokeStyle = 'red';
                ctx.lineWidth = 3;
                ctx.strokeRect(startX, startY, e.offsetX - startX, e.offsetY - startY);
            }}
        }});

        canvas.addEventListener('mouseup', function(e) {{
            isDrawing = false;
            const endX = e.offsetX;
            const endY = e.offsetY;
            const rectWidth = endX - startX;
            const rectHeight = endY - startY;

            if (rectWidth > 0 && rectHeight > 0) {{

                // Đưa thông tin vào div id="rectInfo"
                const rectInfo = 'Hình chữ nhật: X: ' + startX + ', Y: ' + startY + ', Width: ' + rectWidth + ', Height: ' + rectHeight;
                rectInfoDiv.innerHTML = rectInfo;
            }}
        }});
    </script>
    """
    return html

def parse_rect_info(rect_info):
    """Parse rectangle information from the input string."""
    match = re.search(r'Hình chữ nhật: X: (\d+), Y: (\d+), Width: (\d+), Height: (\d+)', rect_info)
    if match:
        x = int(match.group(1))
        y = int(match.group(2))
        w = int(match.group(3))
        h = int(match.group(4))
        return (x, y, w, h)
    return None

def run_app1():
    st.title("Ứng dụng GrabCut")

    # Upload ảnh
    uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Đọc ảnh
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

        # Hiển thị ảnh với canvas overlay
        st.components.v1.html(get_image_with_canvas(image), height=500+50)

        # Nhập thông tin hình chữ nhật từ div (người dùng có thể sao chép hoặc kiểm tra thủ công)
        rect_info = st.text_input("Nhập thông tin hình chữ nhật (nếu có)", "")
        if rect_info:
            rect = parse_rect_info(rect_info)
            if rect:
                x, y, w, h = rect
                rect_coordinates = (x, y, x + w, y + h)

                # Khởi tạo và áp dụng GrabCut
                processor = GrabCutProcessor(image)
                output_image = processor.apply_grabcut(rect=rect_coordinates)
                st.image(output_image, channels="BGR", caption="Kết quả GrabCut")

# Chạy ứng dụng
if __name__ == "__main__":
    run_app1()
