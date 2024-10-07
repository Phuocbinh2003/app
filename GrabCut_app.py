import streamlit as st
import cv2 as cv
import numpy as np
import base64
import re

from grabcut_processor import GrabCutProcessor

def get_image_with_canvas(image, target_width=800):
    """Return HTML for the image with a canvas overlay for drawing."""
    # Encode image as base64
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    # Calculate new dimensions
    height, width = image.shape[:2]
    aspect_ratio = height / width
    target_height = int(target_width * aspect_ratio)

    # HTML for the canvas
    html = f"""
    <div style="position: relative;">
        <img id="image" src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: {target_height}px;"/>
        <canvas id="canvas" style="position: absolute; top: 0; left: 0; width: {target_width}px; height: {target_height}px;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = document.getElementById('image');
        let startX, startY, isDrawing = false;

        canvas.addEventListener('mousedown', function(e) {{
            startX = e.offsetX;
            startY = e.offsetY;
            isDrawing = true;
        }});

        canvas.addEventListener('mousemove', function(e) {{
            if (isDrawing) {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, {target_width}, {target_height});
                ctx.strokeStyle = 'red';
                ctx.lineWidth = 3;
                ctx.strokeRect(startX, startY, e.offsetX - startX, e.offsetY - startY);
            }}
        }});

        canvas.addEventListener('mouseup', function(e) {{
            isDrawing = false;
            const endX = e.offsetX;
            const endY = e.offsetY;
            const rectInfo = 'Hình chữ nhật: X: ' + startX + ', Y: ' + startY + ', Width: ' + (endX - startX) + ', Height: ' + (endY - startY);
            const streamlit = window.parent.document.querySelector('iframe').contentWindow;
            // Dispatching the rectangle information to Streamlit
            streamlit.document.dispatchEvent(new CustomEvent('rectangle-drawn', {{ detail: rectInfo }}));
        }});
    </script>
    """
    return html

def run_app1():
    st.title("GrabCut Application")
    
    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Read image
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        processor = GrabCutProcessor(image)
        
        # Display image with canvas overlay
        st.components.v1.html(get_image_with_canvas(processor.img_copy), height=500)

        # Check for rectangle drawn event
        if 'rectangle-drawn' in st.session_state:
            rect_info = st.session_state.rectangle_drawn.detail
            match = re.search(r'Hình chữ nhật: X: (\d+), Y: (\d+), Width: (\d+), Height: (\d+)', rect_info)
            if match:
                x, y, w, h = map(int, match.groups())
                rect = (x, y, w, h)

                # Apply GrabCut
                if st.button("Apply GrabCut"):
                    output_image = processor.apply_grabcut(rect)
                    st.image(output_image, channels="BGR", caption="GrabCut Output")

                # Display rectangle information
                st.success("Thông tin hình chữ nhật đã được đọc thành công!")
                st.write("Thông tin hình chữ nhật:")
                st.write(f"- X: {x}")
                st.write(f"- Y: {y}")
                st.write(f"- Width: {w}")
                st.write(f"- Height: {h}")
                
        # Reset state after reading the rectangle info
        if 'rectangle-drawn' in st.session_state:
            del st.session_state.rectangle_drawn

# Main function to run the application
if __name__ == "__main__":
    run_app1()
