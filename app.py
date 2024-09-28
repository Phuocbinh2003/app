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
    # Read the image and convert to RGBA
    image = Image.open(uploaded_file).convert("RGBA")
    image_np = np.array(image)  # Convert the image to a NumPy array

    # Check if the image has an alpha channel
    if image_np.ndim == 3 and image_np.shape[2] == 4:
        # Get the dimensions of the original image
        original_height, original_width, _ = image_np.shape

        # Display the uploaded image
        st.image(image, caption="Input Image", use_column_width=True)

        # Set up drawing parameters
        stroke_width = st.sidebar.slider("Stroke Width:", 1, 25, 3)
        stroke_color = st.sidebar.color_picker("Stroke Color:", "#FF0000")

        # Create the canvas with the uploaded image as the background
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",  # Transparent fill color
            stroke_width=stroke_width,      # Stroke width
            stroke_color=stroke_color,      # Stroke color
            background_image=image_np,      # Use uploaded image as background
            update_streamlit=True,
            drawing_mode="freedraw",        # Allow free drawing
            height=original_height,         # Height of the canvas
            width=original_width,           # Width of the canvas
            key="canvas",
            display_toolbar=False            # Hide toolbar for a cleaner UI
        )

        # Show the resulting canvas image if drawn
        if canvas_result.image_data is not None:
            st.image(canvas_result.image_data, caption="Image with Drawings", use_column_width=True)
    
    else:
        st.error("Uploaded image does not have the expected format (RGBA). Please upload a valid image.")

else:
    st.write("Please upload an image.")
