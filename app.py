import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import json
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
                if (event.button === 0) {{ // Left mouse button to start drawing
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
                    ctx.strokeStyle = 'blue';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(Math.min(startX, endX), Math.min(startY, endY), width, height);

                    // Send rectangle coordinates to Python
                    const rect = {{ x: Math.min(startX, endX), y: Math.min(startY, endY), width: width, height: height }};
                    window.parent.postMessage(JSON.stringify(rect), '*');
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
        # Placeholder to receive rectangle coordinates
        rect_data = st.empty()
        rect_data.write("Waiting for rectangle coordinates...")

        # JavaScript to receive the rectangle coordinates
        st.markdown(
            """
            <script>
            window.addEventListener('message', function(event) {
                const rect = JSON.parse(event.data);
                if (rect) {
                    // Send rectangle data to Streamlit
                    const data = { x: rect.x, y: rect.y, width: rect.width, height: rect.height };
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.value = JSON.stringify(data);
                    document.body.appendChild(input);
                    input.dispatchEvent(new Event('change'));
                }
            });
            </script>
            """,
            unsafe_allow_html=True
        )

        # Get rectangle coordinates from the hidden input
        rect_input = st.text_input("Rectangle Coordinates (hidden)", "")
        if rect_input:
            rect_data.write("Rectangle coordinates received.")
            rect_json = json.loads(rect_input)
            x = int(rect_json["x"])
            y = int(rect_json["y"])
            width = int(rect_json["width"])
            height = int(rect_json["height"])
            grabcut_processor.rect = (x, y, width, height)
            grabcut_processor.apply_grabcut()
            output_image = grabcut_processor.get_output_image()
            st.image(output_image, caption="Output Image", use_column_width=True)
