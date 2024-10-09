import streamlit as st
import cv2 as cv
import numpy as np
import base64
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval

def get_image_with_canvas(image):
    """Return HTML with canvas for drawing rectangle."""
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

            if (rectWidth > 0 && rectHeight > 0) {{
                const rectInfo = 'Rectangle: X: ' + startX + ', Y: ' + startY + ', Width: ' + rectWidth + ', Height: ' + rectHeight;
                rectInfoDiv.innerHTML = rectInfo;

                // Send message through postMessage
                window.parent.postMessage({{ rectInfo: rectInfo }}, '*');
            }}
        }});
    </script>
    """
    return html_code

def run_app1():
    st.title("GrabCut Application")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Read image
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

        # Display image with canvas overlay
        html(get_image_with_canvas(image), height=500)

        # JavaScript code to listen for postMessage and send data to Streamlit
        js_code = """
        (function() {
            window.addEventListener('message', (event) => {
                if (event.data && event.data.rectInfo) {
                    const rectInfo = event.data.rectInfo;
                    // Send rectangle info back to Streamlit
                    streamlit.setComponentValue(rectInfo);
                }
            });
        })();
        """

        # Use streamlit_js_eval to listen for events
        streamlit_js_eval(js_code, key="console_key")

        # Display rectangle information drawn
        if st.session_state.get("rect_info"):
            st.write(f"Rectangle information: {st.session_state.rect_info}")

# Run the application
if __name__ == "__main__":
    run_app1()
