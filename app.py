import streamlit as st
from PIL import Image
import base64
import numpy as np

# Function to encode image to base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Configure the Streamlit app
st.set_page_config(layout="wide", page_title="Draw on Image with CSS")

st.title("Upload Image and Draw on It")

# Sidebar to upload the image
st.sidebar.write("## Upload Image")
uploaded_file = st.sidebar.file_uploader("Choose an image to upload", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)
    
    # Convert the image to base64 for embedding in HTML
    image_base64 = convert_image_to_base64(image)

    # HTML and CSS for the drawing canvas
    drawing_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f0f0;
            }}
            canvas {{
                border: 1px solid black;
                cursor: crosshair;
            }}
        </style>
    </head>
    <body>
        <canvas id="drawingCanvas" width="{image.width}" height="{image.height}"></canvas>
        <script>
            const canvas = document.getElementById('drawingCanvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();
            img.src = 'data:image/png;base64,{image_base64}';

            img.onload = function() {{
                ctx.drawImage(img, 0, 0);
            }};

            let drawing = false;

            canvas.addEventListener('mousedown', () => {{
                drawing = true;
            }});

            canvas.addEventListener('mouseup', () => {{
                drawing = false;
                ctx.beginPath();
            }});

            canvas.addEventListener('mousemove', (event) => {{
                if (!drawing) return;
                ctx.lineWidth = 5;
                ctx.lineCap = 'round';
                ctx.strokeStyle = 'red';
                ctx.lineTo(event.offsetX, event.offsetY);
                ctx.stroke();
                ctx.beginPath();
                ctx.moveTo(event.offsetX, event.offsetY);
            }});
        </script>
    </body>
    </html>
    """

    # Render the HTML in Streamlit
    st.components.v1.html(drawing_html, height=image.height)

else:
    st.write("Please upload an image.")
