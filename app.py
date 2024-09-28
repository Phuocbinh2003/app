import streamlit as st
from PIL import Image, ImageDraw

# Configure the Streamlit app
st.set_page_config(layout="wide", page_title="Draw on Image with PIL")

st.title("Upload Image and Draw on It")

# Sidebar to upload the image
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Choose an image to upload", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)

    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Draw a rectangle (example)
    draw.rectangle([(50, 50), (200, 200)], outline="blue", width=5)

    # Display the image
    st.image(image, caption="Image with Drawings", use_column_width=True)

else:
    st.write("Please upload an image.")
