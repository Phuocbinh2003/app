import streamlit as st
import cv2 as cv
import numpy as np
import base64

from GrabCutProcessor import GrabCutProcessor

def get_image_with_canvas(image):
    """Return HTML for the image with a canvas overlay for drawing."""
    # Encode image as base64
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()
    
    # HTML for the canvas
    html = f"""
    <div>
        <img id="image" src="data:image/png;base64,{img_base64}" style="max-width: 100%;"/>
        <canvas id="canvas" style="position: absolute; top: 0; left: 0; width: 100%;"></canvas>
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = document.getElementById('image');
        canvas.width = img.width;
        canvas.height = img.height;

        let startX, startY, isDrawing = false;

        canvas.addEventListener('mousedown', function(e) {{
            startX = e.offsetX;
            startY = e.offsetY;
            isDrawing = true;
        }});

        canvas.addEventListener('mousemove', function(e) {{
            if (isDrawing) {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0);
                ctx.strokeStyle = 'red';
                ctx.lineWidth = 3;
                ctx.strokeRect(startX, startY, e.offsetX - startX, e.offsetY - startY);
            }}
        }});

        canvas.addEventListener('mouseup', function(e) {{
            isDrawing = false;
            const endX = e.offsetX;
            const endY = e.offsetY;
            const rectInfo = `Hình chữ nhật: X: ${startX}, Y: ${startY}, Width: ${endX - startX}, Height: ${endY - startY}`;
            const streamlit = window.parent.document.querySelector('iframe').contentWindow;
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
        image = cv.imdecode(np.fromstring(uploaded_file.read(), np.uint8), 1)
        processor = GrabCutProcessor(image)
        
        # Display image with canvas overlay
        st.components.v1.html(get_image_with_canvas(processor.img_copy), height=500)

        # Listen for rectangle drawn event
        if st.session_state.get('rect_info') is not None:
            rect_info = st.session_state.rect_info
            st.session_state.rect_info = None  # Reset after reading
            match = re.search(r'Hình chữ nhật: X: (\d+), Y: (\d+), Width: (\d+), Height: (\d+)', rect_info)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                w = int(match.group(3))
                h = int(match.group(4))
                rect = (x, y, w, h)
                
                # Apply GrabCut
                if st.button("Apply GrabCut"):
                    output_image = processor.apply_grabcut(rect)
                    st.image(output_image, channels="BGR", caption="GrabCut Output")

        # Add other functionality as needed...

# Main function to run the application
if __name__ == "__main__":
    run_app1()
