import streamlit as st
import cv2 as cv
import numpy as np
import base64
import re

from grabcut_processor import GrabCutProcessor

def get_image_with_canvas(image, target_width=800):
    """Trả về HTML với canvas để vẽ hình chữ nhật."""
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    height, width = image.shape[:2]
    aspect_ratio = height / width
    target_height = int(target_width * aspect_ratio)

    html = f"""
    <div style="position: relative;">
        <img id="image" src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: {target_height}px;"/>
        <canvas id="canvas" style="position: absolute; top: 0; left: 0; width: {target_width}px; height: {target_height}px;"></canvas>
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

            // Chỉ lưu thông tin nếu Width và Height > 0
            if (rectWidth > 0 && rectHeight > 0) {{
                const rectInfo = 'Hình chữ nhật: X: ' + startX + ', Y: ' + startY + ', Width: ' + rectWidth + ', Height: ' + rectHeight;

                // Cập nhật thông tin hình chữ nhật vào div
                rectInfoDiv.innerHTML = rectInfo;

                // Dispatch sự kiện cho Streamlit
                const streamlit = window.parent.document.querySelector('iframe').contentWindow;
                streamlit.document.dispatchEvent(new CustomEvent('rectangle-drawn', {{ detail: rectInfo }}));
            }} else {{
                console.log("Kích thước hình chữ nhật không hợp lệ, bỏ qua.");
            }}
        }});
    </script>
    """
    return html

def run_app():
    st.title("Ứng dụng GrabCut")

    # Upload ảnh
    uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Đọc ảnh
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        processor = GrabCutProcessor(image)

        # Hiển thị ảnh với canvas overlay
        st.components.v1.html(get_image_with_canvas(processor.img_copy), height=500)

        # Kiểm tra và nhận thông tin hình chữ nhật từ session_state
        if 'rect_info' in st.session_state:
            rect_info = st.session_state['rect_info']
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
    run_app()
