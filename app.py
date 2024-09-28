import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
from grabcut_processor import GrabCutProcessor  # Importing the GrabCutProcessor

# Function to encode image to base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Streamlit app
st.title("GrabCut Background Removal with Rectangle Drawing")

# Sidebar for image upload
uploaded_file = st.sidebar.file_uploader("Choose an image to upload", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read the image
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    # Initialize the GrabCut processor
    grabcut_processor = GrabCutProcessor(image_np)

    # HTML and CSS for the drawing canvas
    image_base64 = convert_image_to_base64(image)
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
            let startX, startY;

            canvas.addEventListener('mousedown', (event) => {{
                if (event.button === 2) {{ // Right mouse button
                    drawing = true;
                    startX = event.offsetX;
                    startY = event.offsetY;
                }}
            }});

            canvas.addEventListener('mouseup', (event) => {{
                if (drawing) {{
                    drawing = false;
                    const endX = event.offsetX;
                    const endY = event.offsetY;
                    const width = Math.abs(startX - endX);
                    const height = Math.abs(startY - endY);
                    ctx.rect(startX, startY, width, height);
                    ctx.strokeStyle = 'blue';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                    // Send rectangle coordinates to Python (handle this part with Streamlit)
                }}
            }});
        </script>
    </body>
    </html>
    """

    # Display the canvas
    st.components.v1.html(drawing_html, height=image.height + 100)

    # Button to apply GrabCut
    if st.button("Apply GrabCut"):
        grabcut_processor.apply_grabcut()
        output_image = grabcut_processor.get_output_image()
        st.image(output_image, caption="Output Image", use_column_width=True)
