import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import base64
import cv2 as cv

# Constants for drawing
BLUE = [255, 0, 0]      # Rectangle color
RED = [0, 0, 255]       # PR BG
GREEN = [0, 255, 0]     # PR FG
BLACK = [0, 0, 0]       # Sure BG
WHITE = [255, 255, 255] # Sure FG

# Drawing modes
DRAW_BG = {'color': BLACK, 'val': 0}
DRAW_FG = {'color': WHITE, 'val': 1}
DRAW_PR_FG = {'color': GREEN, 'val': 3}
DRAW_PR_BG = {'color': RED, 'val': 2}

def run_app1():
    st.title("Interactive GrabCut Segmentation")

    # Sidebar to upload image
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        img2 = image_np.copy()  # Copy of the original image
        mask = np.zeros(img2.shape[:2], dtype=np.uint8)  # Mask initialized to PR_BG
        output = np.zeros(img2.shape, np.uint8)  # Output image to be shown

        # Initialize rectangle and drawing flags
        rect = (0, 0, 1, 1)
        drawing = False
        rectangle = False
        rect_over = False
        rect_or_mask = 100
        value = DRAW_FG  # Drawing initialized to FG
        thickness = 3  # Brush thickness

        # HTML and CSS for the drawing canvas
        drawing_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column; 
                    align-items: center; 
                }}
                .canvas-container {{
                    position: relative; 
                    border: 1px solid black; 
                    width: {image.width}px; 
                    height: {image.height}px; 
                }}
                canvas {{
                    cursor: crosshair;
                    position: absolute; 
                    top: 0;
                    left: 0;
                    width: {image.width}px; 
                    height: {image.height}px; 
                    display: block; 
                    z-index: 1; 
                }}
                img {{
                    width: {image.width}px; 
                    height: {image.height}px; 
                    position: absolute; 
                    top: 0;
                    left: 0;
                    z-index: 0; 
                }}
            </style>
        </head>
        <body>
            <div class="canvas-container">
                <img id="originalImage" src="data:image/png;base64,{convert_image_to_base64(image)}" />
                <canvas id="drawingCanvas" width="{image.width}" height="{image.height}"></canvas>
            </div>
            <script>
                const canvas = document.getElementById('drawingCanvas');
                const ctx = canvas.getContext('2d');
                const img = document.getElementById('originalImage');

                let drawing = false;
                let startX, startY;
                let hasDrawnRectangle = false; // Flag to check if rectangle is drawn

                canvas.addEventListener('mousedown', (event) => {{
                    if (event.button === 0 && !hasDrawnRectangle) {{ // Left mouse button
                        drawing = true;
                        startX = event.offsetX;
                        startY = event.offsetY;
                    }}
                    event.preventDefault();
                }});

                canvas.addEventListener('mouseup', (event) => {{
                    if (drawing) {{
                        drawing = false;
                        const endX = event.offsetX;
                        const endY = event.offsetY;
                        const width = Math.abs(startX - endX);
                        const height = Math.abs(startY - endY);

                        const size = Math.min(width, height);
                        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
                        ctx.rect(startX, startY, size, size); // Draw square
                        ctx.strokeStyle = 'blue';
                        ctx.lineWidth = 2;
                        ctx.stroke();

                        const rect = {{ x: Math.min(startX, endX), y: Math.min(startY, endY), width: size, height: size }};
                        hasDrawnRectangle = true; // Mark rectangle drawn
                        window.parent.postMessage(JSON.stringify(rect), '*');
                    }}
                }});

                // Other events for key actions (1, 2, 3, n, r, s)
                document.addEventListener('keydown', (event) => {{
                    // Key handling for foreground/background drawing and segmentation
                    switch(event.key) {{
                        case '0':
                            // Mark background
                            alert('Mark background regions with left mouse button');
                            break;
                        case '1':
                            // Mark foreground
                            alert('Mark foreground regions with left mouse button');
                            break;
                        case '2':
                            // PR_BG drawing
                            break;
                        case '3':
                            // PR_FG drawing
                            break;
                        case 'n':
                            // Update segmentation
                            window.parent.postMessage(JSON.stringify({{action: 'update_segmentation', rect: {{} }} }), '*');
                            break;
                        case 'r':
                            // Reset
                            window.parent.postMessage(JSON.stringify({{action: 'reset' }}), '*');
                            break;
                        case 's':
                            // Save result
                            window.parent.postMessage(JSON.stringify({{action: 'save' }}), '*');
                            break;
                    }}
                }});
            </script>
        </body>
        </html>
        """

        # Display canvas and image
        st.components.v1.html(drawing_html, height=image.height + 50)

        # Update based on messages from JavaScript
        if st.session_state.get("rect_data") is not None:
            rect_data = st.session_state.rect_data
            rect = (rect_data["x"], rect_data["y"], rect_data["width"], rect_data["height"])

            if rect_or_mask == 0:  # GrabCut with rectangle
                bgdmodel = np.zeros((1, 65), np.float64)
                fgdmodel = np.zeros((1, 65), np.float64)
                cv.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_RECT)
                rect_or_mask = 1
            elif rect_or_mask == 1:  # GrabCut with mask
                bgdmodel = np.zeros((1, 65), np.float64)
                fgdmodel = np.zeros((1, 65), np.float64)
                cv.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv.GC_INIT_WITH_MASK)

            mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
            output = cv.bitwise_and(img2, img2, mask=mask2)
            st.image(output, caption="Output Image", use_column_width=True)

        # Instructions
        st.markdown("""
        ## Instructions
        1. Upload an image using the sidebar.
        2. Use the right mouse button to draw a rectangle around the object.
        3. Press 'n' to segment the image.
        4. Press 'r' to reset.
        5. Press 's' to save the result.
        """)

# Convert image to base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Run the application
if __name__ == "__main__":
    run_app1()
