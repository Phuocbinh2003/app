import streamlit as st
import numpy as np
import cv2
from PIL import Image
from streamlit_drawable_canvas import st_canvas

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
        self.value = {'color': (255, 255, 255), 'val': 1}  # Default color is white
        self.thickness = 3

    def run(self):
        if self.img is None:
            st.error("No image uploaded!")
            return

        self.img2 = self.img.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)

        # Display canvas to draw on the image
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

        if canvas_result.json_data is not None:
            objects = canvas_result.json_data.get("objects", [])
            for obj in objects:
                if obj["type"] == "rect":
                    left, top, width, height = map(
                        int, [obj["left"], obj["top"], obj["width"], obj["height"]])
                    self.rect = (left, top, width, height)
                    cv2.rectangle(self.mask, (left, top),
                                  (left + width, top + height), 3, -1)
                elif obj["type"] == "line":
                    x1, y1, x2, y2 = map(
                        int, [obj["x1"], obj["y1"], obj["x2"], obj["y2"]])
                    cv2.line(self.mask, (x1, y1), (x2, y2), 3, 3)
                elif obj["type"] == "path":
                    points = obj["path"]
                    for i in range(len(points) - 1):
                        if all(isinstance(p, list) and len(p) == 2 for p in [points[i], points[i + 1]]):
                            x1, y1 = map(int, points[i])
                            x2, y2 = map(int, points[i + 1])
                            cv2.line(self.mask, (x1, y1),
                                     (x2, y2), 3, 3)

        # Button to run GrabCut
        if st.button("Run GrabCut", type="primary"):
            self.run_grabcut()

        # Button to reset
        if st.button("Reset", type="primary"):
            self.reset_mask()

        # Display result images
        if self.output is not None:
            col1, col2 = st.columns([0.5, 0.5])
            with col1:
                st.image(self.img, caption='Input Image', use_column_width=True)
            with col2:
                st.image(self.output, caption='Segmented Image', use_column_width=True)

    def run_grabcut(self):
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        if self.rect_or_mask == 0:         # GrabCut with rectangle
            cv2.grabCut(self.img2, self.mask, self.rect, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_RECT)
            self.rect_or_mask = 1
        elif self.rect_or_mask == 1:       # GrabCut with mask
            cv2.grabCut(self.img2, self.mask, None, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_MASK)

        mask2 = np.where((self.mask == 1) | (self.mask == 3), 255, 0).astype('uint8')
        self.output = cv2.bitwise_and(self.img2, self.img2, mask=mask2)

    def reset_mask(self):
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="GrabCut Segmentation")

    st.write("# Background Removal with GrabCut")

    st.sidebar.write("## Upload Image")
    uploaded_file = st.sidebar.file_uploader("", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)

        app = GrabCutApp()
        app.img = image.copy()
        st.write("### Results")
        app.run()
