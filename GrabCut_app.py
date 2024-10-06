import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.title("Phân đoạn hình ảnh tương tác bằng GrabCut")

uploaded_file = st.file_uploader("Tải lên hình ảnh", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_np = np.array(img)
    mask = np.zeros(img_np.shape[:2], np.uint8)
    output = np.zeros(img_np.shape, np.uint8)

    # Chọn tọa độ hình chữ nhật (có thể bạn muốn triển khai UI cho điều này)
    x, y, w, h = st.slider("Chọn hình chữ nhật (x, y, chiều rộng, chiều cao)", 0, img_np.shape[1], 0), 0, img_np.shape[0], 0), 0, img_np.shape[1], 1)

    if st.button("Phân đoạn"):
        # Triển khai thuật toán GrabCut ở đây
        bgdmodel = np.zeros((1, 65), np.float64)
        fgdmodel = np.zeros((1, 65), np.float64)
        cv.grabCut(img_np, mask, (x, y, w, h), bgdmodel, fgdmodel, 5, cv.GC_INIT_WITH_RECT)
        
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        output = img_np * mask2[:, :, np.newaxis]

        st.image(output, caption="Hình ảnh đã phân đoạn", use_column_width=True)

