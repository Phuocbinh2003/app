import streamlit as st
import numpy as np
import cv2
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import io

class GrabCutApp:
    def __init__(self):
        self.img = None
        self.img2 = None
        self.mask = None
        self.output = None
        self.rect = (0, 0, 1, 1)
        self.drawing = False
        self.rectangle = False
        self.rect_over = False
        self.rect_or_mask = 100
        self.value = {'color': (255, 255, 255), 'val': 1}  # Màu mặc định là trắng
        self.thickness = 3

    def run(self):
        if self.img is None:
            st.error("Ảnh chưa được tải lên!")
            return

        self.img2 = self.img.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)

        # Hiển thị canvas để vẽ lên ảnh
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=self.thickness,
            stroke_color="#FFFFFF",
            background_image=Image.fromarray(self.img),
            update_streamlit=True,
            height=self.img.shape[0],
            width=self.img.shape[1],
            drawing_mode="freedraw",
            key="canvas",
        )

        # Xử lý các hình dạng vẽ trên canvas
        if canvas_result.json_data is not None:
            objects = canvas_result.json_data.get("objects", [])
            for obj in objects:
                if obj["type"] == "rect":
                    left, top, width, height = map(
                        int, [obj["left"], obj["top"], obj["width"], obj["height"]])
                    self.rect = (left, top, width, height)
                    cv2.rectangle(self.mask, (left, top),
                                  (left + width, top + height), cv2.GC_PR_FGD, -1)
                elif obj["type"] == "line":
                    x1, y1, x2, y2 = map(
                        int, [obj["x1"], obj["y1"], obj["x2"], obj["y2"]])
                    cv2.line(self.mask, (x1, y1), (x2, y2), cv2.GC_BGD, 3)
                elif obj["type"] == "path":
                    points = obj["path"]
                    for i in range(len(points) - 1):
                        if all(isinstance(p, list) and len(p) == 2 for p in [points[i], points[i + 1]]):
                            x1, y1 = map(int, points[i])
                            x2, y2 = map(int, points[i + 1])
                            cv2.line(self.mask, (x1, y1),
                                     (x2, y2), cv2.GC_FGD, 3)

        # Xử lý các sự kiện phím từ URL query
        key = st.experimental_get_query_params().get("key", [None])[0]
        if key:
            if key == 'n':
                self.run_grabcut()
            elif key == 'r':
                self.reset_mask()
            elif key == '0':
                self.value = {'color': (0, 0, 0), 'val': 0}
            elif key == '1':
                self.value = {'color': (255, 255, 255), 'val': 1}
            elif key == '2':
                self.value = {'color': (0, 0, 255), 'val': 2}
            elif key == '3':
                self.value = {'color': (0, 255, 0), 'val': 3}

        if st.button("Chạy GrabCut để phân đoạn", type="primary"):
            self.run_grabcut()

        if st.button("Reset", type="primary"):
            self.reset_mask()

        # Hiển thị ảnh kết quả
        if self.output is not None:
            col1, col2 = st.columns([0.5, 0.5])
            with col1:
                st.image(self.img, caption='Ảnh đầu vào', use_column_width=True)
            with col2:
                st.image(self.output, caption='Ảnh được phân đoạn', use_column_width=True)

    def run_grabcut(self):
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        if self.rect_or_mask == 0:         # grabcut với hình chữ nhật
            cv2.grabCut(self.img2, self.mask, self.rect, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_RECT)
            self.rect_or_mask = 1
        elif self.rect_or_mask == 1:       # grabcut với mask
            cv2.grabCut(self.img2, self.mask, self.rect, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_MASK)

        mask2 = np.where((self.mask == 1) | (self.mask == 3), 255, 0).astype('uint8')
        self.output = cv2.bitwise_and(self.img2, self.img2, mask=mask2)

    def reset_mask(self):
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Deploy GrabCut")

    st.write("# Xóa nền với GrabCut")

    st.sidebar.write("## Tải lên ảnh")
    uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)

        # Hiển thị HTML để xử lý sự kiện phím
        st.markdown("""
            <script>
            document.addEventListener("keydown", function(event) {
                const key = event.key;
                if (['0', '1', '2', '3', 'n', 'r'].includes(key)) {
                    window.parent.postMessage({ key: key }, '*');
                }
            });
            </script>
            """, unsafe_allow_html=True)

        app = GrabCutApp()
        app.img = image.copy()
        st.write("### Kết quả")
        app.run()
