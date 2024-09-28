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

# Displaying instructions
st.markdown("""
### Instructions:
1. **Upload an Image**: Use the sidebar to upload a JPG or PNG image.
2. **Draw a Rectangle**: 
   - Right-click and drag on the canvas to draw a rectangle around the object you want to keep.
   - The rectangle will be outlined in blue.
3. **Apply GrabCut**: Click the "Apply GrabCut" button to remove the background based on the rectangle drawn.
4. **Reset**: If you want to draw a new rectangle or upload a different image, simply refresh the page.

### Features:
- **Image Upload**: Select an image from your local files.
- **Rectangle Drawing**: Draw a rectangle around the area of interest using the right mouse button.
- **Background Removal**: Apply the GrabCut algorithm to segment the foreground from the background.
- **Output Display**: View the processed image with the background removed.

""")

# Sidebar for image upload
uploaded_file = st.sidebar.file_uploader("Choose an image to upload", type=["jpg", "jpeg", "png"])

# Placeholder for rectangle coordinates
rect_coords = st.empty()

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

            canvas.addEventListener('mousemove', (event) => {{
                if (drawing) {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
                    ctx.drawImage(img, 0, 0); // Redraw the image
                    const endX = event.offsetX;
                    const endY = event.offsetY;
                    const width = Math.abs(startX - endX);
                    const height = Math.abs(startY - endY);
                    ctx.strokeStyle = 'blue';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(Math.min(startX, endX), Math.min(startY, endY), width, height);
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
                    const jsonString = JSON.stringify(rect);
                    window.parent.postMessage(jsonString, '*');
                }}
            }});
        </script>
    </body>
    </html>
    """

    # Display the canvas
    st.components.v1.html(drawing_html, height=image.height + 100)

    # JavaScript to receive the rectangle coordinates
    st.markdown(
        """
        <script>
        window.addEventListener('message', function(event) {
            const rect = JSON.parse(event.data);
            if (rect) {
                // Send rectangle data to Streamlit
                const data = {{ x: rect.x, y: rect.y, width: rect.width, height: rect.height }};
                document.body.innerText = JSON.stringify(data);
            }
        });
        </script>
        """,
        unsafe_allow_html=True
    )

    # Button to apply GrabCut
    if st.button("Apply GrabCut"):
        # Get rectangle coordinates
        rect_data = json.loads(st.session_state.get('rect_data', '{}'))
        if rect_data:
            x = int(rect_data['x'])
            y = int(rect_data['y'])
            width = int(rect_data['width'])
            height = int(rect_data['height'])
            grabcut_processor.rect = (x, y, width, height)
            grabcut_processor.apply_grabcut()
            output_image = grabcut_processor.get_output_image()
            st.image(output_image, caption="Output Image", use_column_width=True)

            # Display rectangle coordinates
            st.markdown(f"### Rectangle Coordinates: `x: {x}, y: {y}, width: {width}, height: {height}`")

    # To store the rectangle data
    st.session_state['rect_data'] = rect_coords.empty()
