import streamlit as st
import cv2 as cv
import numpy as np
from streamlit_drawable_canvas import st_canvas

def run_app1():
    st.title("Ứng dụng GrabCut")

    # Tải lên hình ảnh
    uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "png"])
    if uploaded_file is not None:
        # Đọc hình ảnh
        image = cv.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)

        # Hiển thị hình ảnh
        st.image(image, channels="BGR", caption="Ảnh gốc", use_column_width=True)

        # Tạo canvas để vẽ hình chữ nhật
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",  # Transparent fill
            stroke_width=3,
            stroke_color="red",
            background_image=st.image(image, channels="BGR"),
            update_streamlit=True,
            width=image.shape[1],
            height=image.shape[0],
            drawing_mode="rect",
            key="canvas",
        )

        # Lấy tọa độ của hình chữ nhật được vẽ
        if canvas_result.json_data is not None:
            for shape in canvas_result.json_data["objects"]:
                if shape["type"] == "rect":
                    rect = shape
                    left = rect["left"]
                    top = rect["top"]
                    width = rect["width"]
                    height = rect["height"]

                    # Hiển thị thông tin tọa độ
                    st.write(f"Hình chữ nhật: X: {left}, Y: {top}, Width: {width}, Height: {height}")

                    # Ứng dụng thuật toán GrabCut
                    rect_coords = (int(left), int(top), int(left + width), int(top + height))
                    segmented_image = apply_grabcut(image, rect_coords)
                    
                    # Hiển thị hình ảnh sau khi áp dụng GrabCut
                    st.image(segmented_image, channels="BGR", caption="Hình ảnh sau khi áp dụng GrabCut", use_column_width=True)

def apply_grabcut(image, rect):
    # Tạo mặt nạ cho ảnh
    mask = np.zeros(image.shape[:2], np.uint8)
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    # Áp dụng GrabCut
    cv.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv.GC_INIT_WITH_RECT)

    # Tạo mặt nạ nhị phân
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype("uint8")

    # Áp dụng mặt nạ lên ảnh gốc
    result = image * mask2[:, :, np.newaxis]

    return result

# Chạy ứng dụng
if __name__ == "__main__":
    run_app1()
