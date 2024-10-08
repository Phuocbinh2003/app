import streamlit as st
import cv2 as cv
import numpy as np
import base64
import re

def get_image_with_canvas(image):
    """Return HTML with canvas to draw a rectangle."""
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    height, width = image.shape[:2]

    html = f"""
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

            if (rectWidth > 0 && rectHeight > 0) {{
                const rectInfo = 'Hình chữ nhật: X: ' + startX + ', Y: ' + startY + ', Width: ' + rectWidth + ', Height: ' + rectHeight;
                rectInfoDiv.innerHTML = rectInfo;

                // Send rectangle info back to Streamlit
                const streamlitDiv = document.createElement('div');
                streamlitDiv.setAttribute('data-rect-info', rectInfo);
                document.body.appendChild(streamlitDiv);
                const event = new Event('rectInfoEvent');
                streamlitDiv.dispatchEvent(event);
            }}
        }});
    </script>
    """
    return html

def run_app1():
    st.title("Ứng dụng GrabCut")

    # Upload image
    uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Read image
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

        # Display image with canvas overlay
        st.components.v1.html(get_image_with_canvas(image), height=500)

        # Listen for rectangle info from iframe
        rect_info = st.session_state.get('rect_info', None)
        if rect_info is not None:
            st.write(f"Thông tin hình chữ nhật: {rect_info}")
            match = re.search(r'Hình chữ nhật: X: (\d+), Y: (\d+), Width: (\d+), Height: (\d+)', rect_info)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                w = int(match.group(3))
                h = int(match.group(4))
                rect = (x, y, w, h)

                # Apply GrabCut button
                if st.button("Áp dụng GrabCut"):
                    mask = np.zeros(image.shape[:2], np.uint8)
                    bgd_model = np.zeros((1, 65), np.float64)
                    fgd_model = np.zeros((1, 65), np.float64)
                    rect = (x, y, x + w, y + h)
                    cv.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv.GC_INIT_WITH_RECT)
                    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
                    output_image = image * mask2[:, :, np.newaxis]
                    st.image(output_image, channels="BGR", caption="Kết quả GrabCut")

# Run the app
if __name__ == "__main__":
    run_app1()
