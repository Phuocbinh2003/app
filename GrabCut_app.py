import streamlit as st
import cv2 as cv
import numpy as np
import base64
import re
from streamlit_js_eval import streamlit_js_eval

from grabcut_processor import GrabCutProcessor

# Hàm lấy ảnh với canvas
def get_image_with_canvas(image):
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    height, width = image.shape[:2]

    html = f"""
    <div style="position: relative;">
        <img id="image" src="data:image/png;base64,{img_base64}" style="width: {width}px; height: {height}px;"/>
        <canvas id="canvas" width="{width}" height="{height}" style="position: absolute; top: 0; left: 0; border: 1px solid red;"></canvas>
        <div id="rectInfo" style="margin-top: 10px;"></div> <!-- Nơi lưu thông tin hình chữ nhật -->
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
                const rectInfo = 'Hình chữ nhật: X: ' + startX + ', Y: ' + startY + ', Width: ' + rectWidth + ', Height: ' + rectHeight;
                rectInfoDiv.innerHTML = rectInfo;

                // Chuyển kết quả cho phần tử HTML
                window.rect_info = rectInfo;
            }} else {{
                console.log("Kích thước hình chữ nhật không hợp lệ, bỏ qua.");
            }}
        }});
    </script>
    """
    return html

# Hàm chạy ứng dụng
def run_app1():
    st.title("Ứng dụng GrabCut")

    # Upload ảnh
    uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Đọc ảnh
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        processor = GrabCutProcessor(image)

        # Hiển thị ảnh với canvas overlay
        st.components.v1.html(get_image_with_canvas(processor.img_copy), height=500)

        # Đọc dữ liệu từ div 'rectInfo'
        rect_info = streamlit_js_eval(code="document.getElementById('rectInfo').innerHTML", key="rect_info")

        if rect_info and "Hình chữ nhật" in rect_info:
            st.write(f"Thông tin hình chữ nhật: {rect_info}")
            match = re.search(r'Hình chữ nhật: X: (\d+), Y: (\d+), Width: (\d+), Height: (\d+)', rect_info)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                w = int(match.group(3))
                h = int(match.group(4))
                rect = (x, y, w, h)

                # Nút áp dụng GrabCut
                if st.button("Áp dụng GrabCut"):
                    output_image = processor.apply_grabcut(rect)
                    st.image(output_image, channels="BGR", caption="Kết quả GrabCut")

# Chạy ứng dụng
if __name__ == "__main__":
    run_app1()
