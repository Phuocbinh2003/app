import streamlit as st
import cv2 as cv
import numpy as np
import base64
import re
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval

def get_image_with_canvas(image):
    """Return HTML with canvas to draw a rectangle."""
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    height, width = image.shape[:2]

    html_code = f"""
    <div style="position: relative;">
        <img id="image" src="data:image/png;base64,{img_base64}" style="width: {width}px; height: {height}px;"/>
        <canvas id="canvas" width="{width}" height="{height}" style="position: absolute; top: 0; left: 0; border: 1px solid red;"></canvas>
        <div id="rectInfo" style="margin-top: 10px;"></div>
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
            console.log('Mouse up event:', startX, startY, rectWidth, rectHeight);

            if (rectWidth > 0 && rectHeight > 0) {{
                const rectInfo = 'Hình chữ nhật: X: ' + startX + ', Y: ' + startY + ', Width: ' + rectWidth + ', Height: ' + rectHeight;
                rectInfoDiv.innerHTML = rectInfo;

                // Gửi thông điệp qua postMessage
                window.parent.postMessage({{ rectInfo: rectInfo }}, '*');
            }}
        }});
    </script>
    """
    return html_code

def run_app1():
    st.title("Ứng dụng GrabCut")

    # Upload image
    uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Read image
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

        # Display image with canvas overlay
        html(get_image_with_canvas(image), height=500)

        # Lắng nghe console log và hiển thị trên Streamlit
        js_code = """
        (function() {
            window.addEventListener('message', (event) => {
                if (event.data && event.data.rectInfo) {
                    const rectInfo = event.data.rectInfo;
                    console.log('Mouse up event:', rectInfo);
                    streamlitWebSocket.send(rectInfo);
                }
            });
        })();
        """
        
        # Chạy đoạn mã JavaScript để lắng nghe thông điệp từ postMessage
        rect_info = streamlit_js_eval(js_code, key="console_key", label="rect_info_listener")

        # Nếu có thông tin từ console
        if rect_info:
            st.write(f"Console log: {rect_info}")

# Run the app
if __name__ == "__main__":
    run_app1()
