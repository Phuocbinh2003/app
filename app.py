import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import json
from grabcut_processor import GrabCutProcessor  # Import GrabCutProcessor

# Function to encode image to base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Streamlit app
st.title("Xóa nền bằng GrabCut với các công cụ vẽ")

# Sidebar for image upload
uploaded_file = st.sidebar.file_uploader("Chọn một hình ảnh để tải lên", type=["jpg", "jpeg", "png"])

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
                if (event.button === 2) {{ // Chuột phải
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
                    ctx.clearRect(0, 0, canvas.width, canvas.height); // Xóa canvas trước khi vẽ lại
                    ctx.drawImage(img, 0, 0); // Vẽ lại hình ảnh
                    ctx.rect(startX, startY, width, height);
                    ctx.strokeStyle = 'blue';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    // Gửi tọa độ hình chữ nhật đến Python
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

    # Placeholder to store rectangle coordinates
    rect_coords = st.empty()

    # JavaScript to receive the rectangle coordinates
    st.markdown(
        """
        <script>
        window.addEventListener('message', function(event) {
            const rect = JSON.parse(event.data);
            if (rect) {{
                // Gửi dữ liệu hình chữ nhật về Streamlit
                document.body.innerText = JSON.stringify(rect);
            }}
        });
        </script>
        """,
        unsafe_allow_html=True
    )

    # Button to apply GrabCut
    if st.button("Áp dụng GrabCut"):
        # Get rectangle coordinates
        rect_data = st.session_state.get('rect', None)
        if rect_data is not None:
            rect = json.loads(rect_data)
            x = int(rect['x'])
            y = int(rect['y'])
            width = int(rect['width'])
            height = int(rect['height'])
            grabcut_processor.rect = (x, y, width, height)
            grabcut_processor.apply_grabcut()
            output_image = grabcut_processor.get_output_image()
            st.image(output_image, caption="Hình ảnh sau khi cắt nền", use_column_width=True)

    # Instructions
    st.sidebar.markdown("""
    ## Hướng dẫn sử dụng
    1. Tải lên một hình ảnh bằng cách sử dụng mục tải lên bên trái.
    2. Sử dụng chuột phải để vẽ một hình chữ nhật xung quanh vùng bạn muốn giữ lại.
    3. Nhấn nút **Áp dụng GrabCut** để cắt nền hình ảnh.
    4. Bạn có thể sử dụng các công cụ khác như:
       - Vẽ vùng foreground (nền chính) bằng chuột trái.
       - Vẽ vùng background (nền phụ) bằng cách vẽ với màu khác.
       - Vẽ hình chữ nhật để chọn vùng cắt.
       - Nhấn nút **Đặt lại** để khôi phục hình ảnh gốc và bắt đầu lại.
    """)
