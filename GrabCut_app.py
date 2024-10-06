import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import numpy as np
import cv2 as cv

# Import GrabCutProcessor
from grabcut_processor import GrabCutProcessor

# Helper function to convert image to base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Main function to run the Streamlit app
def run_app():
    st.title("Interactive GrabCut Segmentation")

    # Sidebar to upload image
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_np = np.array(image)

        # Initialize the GrabCutProcessor
        grabcut_processor = GrabCutProcessor(img_np)

        # HTML and JS for drawing
        drawing_html = f"""
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
        </body>
        </html>
        """

        st.components.v1.html(drawing_html, height=image.height + 50)

        # Handle JavaScript events from the canvas
        if "rect_data" in st.session_state:
            rect_data = st.session_state.rect_data
            rect = (rect_data["x"], rect_data["y"], rect_data["width"], rect_data["height"])

            # Apply GrabCut using the rectangle
            output_img = grabcut_processor.apply_grabcut(rect)
            st.image(output_img, caption="GrabCut Output", use_column_width=True)

        if "reset" in st.session_state:
            # Reset the image
            reset_img = grabcut_processor.reset()
            st.image(reset_img, caption="Reset Image", use_column_width=True)

        # Handle the drawing value changes (0, 1, 2, 3)
        if "set_drawing_value" in st.session_state:
            grabcut_processor.set_drawing_value(st.session_state.set_drawing_value)

        # Instructions for the user
        st.markdown("""
        ### Instructions
        1. Upload an image using the sidebar.
        2. Use mouse to draw a rectangle around the object.
        3. Press the following keys:
            - `0`: Mark definite background
            - `1`: Mark definite foreground
            - `2`: Mark probable background
            - `3`: Mark probable foreground
            - `n`: Apply GrabCut
            - `r`: Reset the image
        """)

if __name__ == "__main__":
    run_app()
