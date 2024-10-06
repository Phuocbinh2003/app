import streamlit as st
from PIL import Image
import numpy as np
import cv2
from grabcut_processor import GrabCutProcessor

def run_app1():
    st.title("Cắt nền bằng GrabCut")

    # Sidebar for image upload
    uploaded_file = st.sidebar.file_uploader("Chọn hình ảnh", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Read the image
        image = Image.open(uploaded_file)
        image_np = np.array(image)

        # Initialize GrabCut processor
        grabcut_processor = GrabCutProcessor(image_np)

        # Show the image
        st.image(image, caption="Hình ảnh gốc", use_column_width=True)

        # Create a drawing canvas
        drawing_area = st.empty()
        canvas = drawing_area.image(grabcut_processor.img, channels="RGB")

        # Mouse event handling for rectangle drawing and mask
        # This would require OpenCV to handle events which may not work in Streamlit directly
        # Therefore, consider using JavaScript as shown in the previous example to handle mouse events

        # Button to apply GrabCut
        if st.button("Áp dụng GrabCut"):
            grabcut_processor.apply_grabcut()
            output_image = grabcut_processor.get_output_image()
            st.image(output_image, caption="Hình ảnh đầu ra", use_column_width=True)

        # Instructions
        st.markdown("""
        ## Hướng dẫn sử dụng
        1. Tải lên một hình ảnh bằng cách sử dụng menu ở bên trái.
        2. Nhấn chuột trái để vẽ hình chữ nhật quanh đối tượng bạn muốn cắt.
        3. Nhấn nút "Áp dụng GrabCut" để cắt nền.
        """)

# Bước 8: Chạy ứng dụng
if __name__ == "__main__":
    run_app1()
