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

        # Get image dimensions and scale
        height, width, _ = self.img.shape
        max_dim = 800  # Max dimension for canvas
        scale = min(max_dim / width, max_dim / height)
        new_width = int(width * scale)
        new_height = int(height * scale)

        # Resize image to fit within the canvas
        img_resized = cv2.resize(self.img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        self.img2 = img_resized.copy()
        self.mask = np.zeros(img_resized.shape[:2], dtype=np.uint8)
        self.output = np.zeros(img_resized.shape, np.uint8)

        # Display canvas to draw on the image
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",
            stroke_width=self.thickness,
            stroke_color="#FFFFFF",
            background_image=Image.fromarray(img_resized),
            update_streamlit=True,
            height=new_height,
            width=new_width,
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

        # Buttons to interact with the app
        if st.button("Run GrabCut"):
            self.run_grabcut()

        if st.button("Reset"):
            self.reset_mask()

        # Display both images overlaid
        if self.img is not None:
            # Create a canvas for displaying the result
            result_img = np.copy(self.img)
            if self.output is not None:
                # Overlay the segmented output on the input image
                mask_overlay = np.zeros(self.img.shape, dtype=np.uint8)
                mask_overlay[:, :, :3] = self.output
                result_img = cv2.addWeighted(result_img, 0.7, mask_overlay, 0.3, 0)

            # Ensure the image fits within the canvas dimensions
            st.image(result_img, caption='Segmented Image', use_column_width=True)

    def run_grabcut(self):
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)

        if self.rect_or_mask == 0:         # GrabCut with rectangle
            cv2.grabCut(self.img2, self.mask, self.rect, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_RECT)
            self.rect_or_mask = 1
        elif self.rect_or_mask == 1:       # GrabCut with mask
            cv2.grabCut(self.img2, self.mask, self.rect, bgd_model, fgd_model, 1, cv2.GC_INIT_WITH_MASK)

        mask2 = np.where((self.mask == 1) | (self.mask == 3), 255, 0).astype('uint8')
        self.output = cv2.bitwise_and(self.img2, self.img2, mask=mask2)

    def reset_mask(self):
        self.rect = (0, 0, 1, 1)
        self.drawing = False
        self.rectangle = False
        self.rect_or_mask = 100
        self.rect_over = False
        self.value = {'color': (255, 255, 255), 'val': 1}
        self.img = self.img2.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)

# Streamlit application entry point
def main():
    st.title("GrabCut Segmentation")
    upload_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    
    if upload_file is not None:
        image = Image.open(upload_file)
        image = np.array(image.convert('RGB'))  # Convert to RGB
        
        app = GrabCutApp()
        app.img = image
        app.run()

if __name__ == "__main__":
    main()
