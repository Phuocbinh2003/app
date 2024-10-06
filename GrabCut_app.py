import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import numpy as np
import cv2 as cv

# Import lớp GrabCutProcessor từ file grabcut_processor
from grabcut_processor import GrabCutProcessor

def run_app1():
    st.title("GrabCut Segmentation with Streamlit Drawable Canvas")

    # Sidebar to upload an image
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(uploaded_file)
        img_np = np.array(image)

        # Initialize the GrabCutProcessor
        grabcut_processor = GrabCutProcessor(img_np)

        # Streamlit Drawable Canvas
        st.sidebar.markdown("### Drawing Tools")
        drawing_mode = st.sidebar.selectbox(
            "Drawing tool:", ("rectangle", "freedraw")
        )
        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)

        # Create a canvas component for drawing
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Color for the rectangle or mask
            stroke_width=stroke_width,
            stroke_color="#FF0000",
            background_image=image,
            update_streamlit=True,
            height=image.height,
            width=image.width,
            drawing_mode=drawing_mode,
            key="canvas",
        )

        # After drawing, apply GrabCut based on the drawn region
        if canvas_result.json_data is not None:
            # Extract rectangle coordinates from the drawn shape
            for shape in canvas_result.json_data["objects"]:
                if shape["type"] == "rect":
                    left = shape["left"]
                    top = shape["top"]
                    width = shape["width"]
                    height = shape["height"]
                    rect = (int(left), int(top), int(width), int(height))

                    # Apply GrabCut with the selected rectangle
                    output_img = grabcut_processor.apply_grabcut(rect)
                    st.image(output_img, caption="GrabCut Result", use_column_width=True)

        # Option to reset the image
        if st.button("Reset"):
            reset_img = grabcut_processor.reset()
            st.image(reset_img, caption="Image Reset", use_column_width=True)

        # Instructions for user
        st.markdown("""
        ### Instructions:
        1. Draw a rectangle around the object you want to segment.
        2. Select "rectangle" mode in the sidebar for precise bounding box drawing.
        3. Adjust the stroke width as needed.
        4. After drawing, the segmentation result will automatically appear below.
        5. Use the "Reset" button to start over.
        """)

if __name__ == "__main__":
    run_app1()
