import streamlit as st
import cv2 as cv
import numpy as np
import base64
import re
from grabcut_processor import GrabCutProcessor

class GrabCutData:
    def __init__(self):
        self.rect = None

    def set_rectangle(self, rect):
        self.rect = rect

    def clear(self):
        self.rect = None

# Tạo đối tượng GrabCutData
grabcut_data = GrabCutData()

def get_image_with_canvas(image, target_width=800):
    """Return HTML for the image with a canvas overlay for drawing."""
    # Encode image as base64
    _, img_encoded = cv.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode()

    # Tính toán tỷ lệ kích thước mới
    height, width = image.shape[:2]
    aspect_ratio = height / width
    target_height = int(target_width * aspect_ratio)

    # HTML for the canvas
    html = f"""
    <div style="position: relative;">
        <img id="image" src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: {target_height}px;"/>
        <canvas id="canvas" style="position: absolute; top: 0; left: 0; width: {target_width}px; height: {target_height}px;"></canvas>
        <input type="hidden" id="rectInfo" value="" /> <!-- Input ẩn để lưu trữ thông tin hình chữ nhật -->
    </div>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const img = document.getElementById('image');
        canvas.width = {target_width};
        canvas.height = {target_height};

        let startX, startY, isDrawing = false;

        canvas.addEventListener('mousedown', function(e) {{
            startX = e.offsetX;
            startY = e.offsetY;
            isDrawing = true;
        }});

        canvas.addEventListener('mousemove', function(e) {{
            if (isDrawing) {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0, {target_width}, {target_height});
                ctx.strokeStyle = 'red';
                ctx.lineWidth = 3;
                ctx.strokeRect(startX, startY, e.offsetX - startX, e.offsetY - startY);
            }}
        }});

        canvas.addEventListener('mouseup', function(e) {{
            isDrawing = false;
            const endX = e.offsetX;
            const endY = e.offsetY;
            const rectInfo = 'Hình chữ nhật: X: ' + startX + ', Y: ' + startY + ', Width: ' + (endX - startX) + ', Height: ' + (endY - startY);
            const rectInput = document.getElementById('rectInfo');
            rectInput.value = rectInfo; // Lưu thông tin hình chữ nhật vào input ẩn
            const streamlit = window.parent.document.querySelector('iframe').contentWindow;
            streamlit.document.dispatchEvent(new CustomEvent('rectangle-drawn', {{ detail: rectInfo }}));
        }});
    </script>
    """
    return html

def run_app1():
    st.title("GrabCut Application")
    
    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if uploaded_file is not None:
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        processor = GrabCutProcessor(image)
        
        # Display image with canvas overlay
        st.components.v1.html(get_image_with_canvas(processor.img_copy), height=500)

        # Kiểm tra thông tin hình chữ nhật từ session_state
        if 'rect_info' in st.session_state:
            rect_info = st.session_state.rect_info
            if rect_info is not None:
                match = re.search(r'Hình chữ nhật: X: (\d+), Y: (\d+), Width: (\d+), Height: (\d+)', rect_info)
                if match:
                    x = int(match.group(1))
                    y = int(match.group(2))
                    w = int(match.group(3))
                    h = int(match.group(4))
                    rect = (x, y, w, h)

                    # Lưu trữ hình chữ nhật vào đối tượng GrabCutData
                    grabcut_data.set_rectangle(rect)

                    # Hiển thị thông tin hình chữ nhật
                    st.success("Thông tin hình chữ nhật đã được đọc thành công!")
                    st.write("Thông tin hình chữ nhật:")
                    st.write(f"- X: {x}")
                    st.write(f"- Y: {y}")
                    st.write(f"- Width: {w}")
                    st.write(f"- Height: {h}")

                    # Hiển thị nút Apply GrabCut nếu hình chữ nhật đã được xác định
                    if st.button("Apply GrabCut"):
                        output_image = processor.apply_grabcut(grabcut_data.rect)
                        st.image(output_image, channels="BGR", caption="GrabCut Output")
                else:
                    st.error("Không thể đọc thông tin hình chữ nhật!")
            else:
                st.warning("Chưa có thông tin hình chữ nhật.")

        # Reset rectangle info after reading
        st.session_state.rect_info = None

# Main function to run the application
if __name__ == "__main__":
    run_app1()
