import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import numpy as np

# Configure the Streamlit app
st.set_page_config(layout="wide", page_title="Draw on Image")

st.title("Upload Image and Draw on It")

# Sidebar to upload the image
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Choose an image to upload", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)
    image_np = np.array(image)  # Convert the image to a NumPy array

    # Get the dimensions of the original image
    original_width, original_height = image.size

    # Set the maximum canvas size based on the uploaded image
    max_canvas_width = st.sidebar.slider("Max Canvas Width (px):", 300, 1200, original_width)
    ratio = max_canvas_width / original_width
    new_height = int(original_height * ratio)

    # Display the uploaded image
    st.image(image, caption="Input Image", use_column_width=False, width=max_canvas_width)

    # Set up drawing parameters
    stroke_width = st.sidebar.slider("Stroke Width:", 1, 25, 3)
    stroke_color = st.sidebar.color_picker("Stroke Color:", "#FF0000")

    # Create the canvas with the image as the background
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 0)",  # Transparent fill color
        stroke_width=stroke_width,      # Stroke width
        stroke_color=stroke_color,      # Stroke color
        background_image=Image.fromarray(image_np),  # Background image
        update_streamlit=True,
        drawing_mode="rect",            # Allow drawing rectangles
        height=new_height,              # Height of the canvas
        width=max_canvas_width,         # Width of the canvas
        key="canvas",
    )

    # Show the resulting canvas image if drawn
    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data, caption="Image with Drawings", use_column_width=False, width=max_canvas_width)

else:
    st.write("Please upload an image.")
