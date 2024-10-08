import streamlit as st
import cv2 as cv
import numpy as np
import base64

from grabcut_processor import GrabCutProcessor

def get_image_with_canvas(image):
    """Trả về HTML với canvas để vẽ hình chữ nhật."""
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    height, width = image.shape[:2]

    html = f"""
    <div style="position: relative;">
        <img id="image" src="data:image/png;base64,{img_base64}" style="width: {width}px; height: {height}px;"/>
        <canvas id="canvas" width="{width}" height="{height}" style="position: absolute; top: 0; left: 0; border: 1px solid red;"></canvas>
        <div id="rectInfo" style="margin-top: 10px;"> <!-- Nơi lưu thông tin hình chữ nhật -->
        </div>
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

                // Gửi thông tin hình chữ nhật về phía Streamlit qua window.postMessage
                window.parent.postMessage({{
                    startX: startX,
                    startY: startY,
                    rectWidth: rectWidth,
                    rectHeight: rectHeight
                }}, "*");
            }} else {{
                console.log("Kích thước hình chữ nhật không hợp lệ, bỏ qua.");
            }}
        }});
    </script>
    """
    return html

def run_app1():
    st.title("Ứng dụng GrabCut")

    # Upload ảnh
    uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Đọc ảnh
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        processor = GrabCutProcessor(image)

        # Nhận nội dung HTML
        html_content = get_image_with_canvas(processor.img_copy)

        # Hiển thị ảnh với canvas overlay
        st.components.v1.html(html_content, height=500)

        # Nhận thông tin từ window.postMessage
        message = st.experimental_get_query_params()
        if message:
            try:
                startX = int(message.get("startX")[0])
                startY = int(message.get("startY")[0])
                rectWidth = int(message.get("rectWidth")[0])
                rectHeight = int(message.get("rectHeight")[0])

                st.write(f"Thông tin hình chữ nhật: X: {startX}, Y: {startY}, Width: {rectWidth}, Height: {rectHeight}")

                # Nút áp dụng GrabCut
                if st.button("Áp dụng GrabCut"):
                    rect = (startX, startY, rectWidth, rectHeight)
                    output_image = processor.apply_grabcut(rect)
                    st.image(output_image, channels="BGR", caption="Kết quả GrabCut")

            except (TypeError, ValueError):
                st.write("Chưa có thông tin hình chữ nhật được truyền về.")

# Chạy ứng dụng
if __name__ == "__main__":
    run_app1()
