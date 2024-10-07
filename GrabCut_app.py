import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
import base64
from grabcut_processor import GrabCutProcessor

def run_app1():
    st.title("Cắt nền bằng GrabCut")

    # Thanh bên để tải lên hình ảnh
    uploaded_file = st.sidebar.file_uploader("Chọn hình ảnh", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Đọc hình ảnh
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        # Khởi tạo bộ xử lý GrabCut
        grabcut_processor = GrabCutProcessor(image_np)

        # Lấy kích thước của hình ảnh
        img_width, img_height = image.size

        # HTML và CSS cho việc vẽ
        drawing_html = f"""
        <!DOCTYPE html>
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
                    width: {img_width}px; 
                    height: {img_height}px; 
                }}
                canvas {{
                    cursor: crosshair;
                    position: absolute; 
                    top: 0;
                    left: 0;
                    width: {img_width}px; 
                    height: {img_height}px; 
                    display: block; 
                    z-index: 1; 
                }}
                img {{
                    width: {img_width}px; 
                    height: {img_height}px; 
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
                <canvas id="drawingCanvas" width="{img_width}" height="{img_height}"></canvas>
            </div>
            <script>
                const canvas = document.getElementById('drawingCanvas');
                const ctx = canvas.getContext('2d');
                const img = document.getElementById('originalImage');

                let drawing = false;
                let startX, startY;
                let hasDrawnRectangle = false;

                canvas.addEventListener('mousedown', (event) => {{
                    if (event.button === 0 && !hasDrawnRectangle) {{
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
                        
                        ctx.clearRect(0, 0, canvas.width, canvas.height); 
                        ctx.rect(startX, startY, width, height); 
                        ctx.strokeStyle = 'blue';
                        ctx.lineWidth = 2;
                        ctx.stroke();

                        const rect = {{ x: Math.min(startX, endX), y: Math.min(startY, endY), width: width, height: height }};
                        hasDrawnRectangle = true;
                        
                        // Lưu vào localStorage
                        localStorage.setItem('rect_data', JSON.stringify(rect));
                    }}
                }});

                // Kiểm tra localStorage để lấy dữ liệu hình chữ nhật
                const savedRectData = localStorage.getItem('rect_data');
                if (savedRectData) {{
                    const rect = JSON.parse(savedRectData);
                    console.log("Saved Rectangle Data: ", rect);
                }}
            </script>
        </body>
        </html>
        """

        # Hiển thị canvas và hình ảnh
        st.components.v1.html(drawing_html, height=img_height + 50)

        # Khởi tạo bộ xử lý GrabCut
        if uploaded_file is not None:
            # Kiểm tra dữ liệu hình chữ nhật trong localStorage
            rect_data = st.session_state.get("rect_data", None)

            if st.button("Áp dụng GrabCut"):
                # Lấy dữ liệu hình chữ nhật từ localStorage
                if st.session_state.rect_data:
                    rect_data = st.session_state.rect_data
                    x = int(rect_data["x"])
                    y = int(rect_data["y"])
                    width = int(rect_data["width"])
                    height = int(rect_data["height"])
                    grabcut_processor.rect = (x, y, width, height)

                    # Áp dụng GrabCut
                    grabcut_processor.apply_grabcut()
                    output_image = grabcut_processor.get_output_image()
                    st.image(output_image, caption="Hình ảnh đầu ra", use_column_width=True)
                else:
                    st.warning("Vui lòng vẽ một hình chữ nhật trước khi áp dụng GrabCut.")

        # Hướng dẫn sử dụng
        st.markdown(""" 
        ## Hướng dẫn sử dụng 
        1. Tải lên một hình ảnh bằng cách sử dụng menu ở bên trái. 
        2. Nhấn chuột trái để vẽ hình chữ nhật quanh đối tượng bạn muốn cắt. 
        3. Nhấn nút "Áp dụng GrabCut" để cắt nền. 
        """)

# Hàm để mã hóa hình ảnh thành base64
def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Bước 8: Chạy ứng dụng
if __name__ == "__main__":
    run_app1()
