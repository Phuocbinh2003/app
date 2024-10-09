import streamlit as st
import cv2 as cv
import numpy as np
import base64
from streamlit_js_eval import streamlit_js_eval

def get_image_with_canvas(image):
    """Trả về HTML với canvas để vẽ hình chữ nhật."""
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    height, width = image.shape[:2]

    html_code = f"""
    <div style="position: relative;">
        <img id="image" src="data:image/png;base64,{img_base64}" style="width: {width}px; height: {height}px;"/>
        <canvas id="canvas" width="{width}" height="{height}" style="position: absolute; top: 0; left: 0; border: 1px solid red;"></canvas>
        <div id="streamlit_rect_info" style="margin-top: 10px;"></div>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = document.getElementById('image');
        let startX, startY, endX, endY, isDrawing = false;

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
            endX = e.offsetX;
            endY = e.offsetY;
            const rectWidth = endX - startX;
            const rectHeight = endY - startY;

            if (rectWidth > 0 && rectHeight > 0) {{
                const rectInfo = `X: ${startX}, Y: ${startY}, Width: ${rectWidth}, Height: ${rectHeight}`;
                document.getElementById('streamlit_rect_info').innerText = rectInfo;

                // Gửi thông tin hình chữ nhật về Streamlit
                streamlitWebEval(rectInfo);
            }}
        }});
    </script>
    """
    return html_code

def run_app1():
    st.title("Ứng dụng GrabCut")

    # Tải lên hình ảnh
    uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Đọc hình ảnh
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

        # Hiển thị hình ảnh với lớp phủ canvas
        st.components.v1.html(get_image_with_canvas(image), height=image.shape[0] + 200)

        # Nhận thông tin hình chữ nhật từ JavaScript
        rect_info = streamlit_js_eval('document.getElementById("streamlit_rect_info").innerText')

        if rect_info:
            st.write(f"Tọa độ hình chữ nhật: {rect_info}")
            # Bạn có thể tiếp tục xử lý tọa độ ở đây để áp dụng thuật toán GrabCut

# Chạy ứng dụng
if __name__ == "__main__":
    run_app1()
