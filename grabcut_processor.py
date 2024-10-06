import numpy as np
import cv2

class GrabCutProcessor:
    BLUE = [255, 0, 0]        # Màu cho hình chữ nhật
    RED = [0, 0, 255]         # Màu cho dự đoán nền
    GREEN = [0, 255, 0]       # Màu cho dự đoán foreground
    BLACK = [0, 0, 0]         # Màu cho nền chắc chắn
    WHITE = [255, 255, 255]   # Màu cho foreground chắc chắn

    DRAW_BG = {'color': BLACK, 'val': 0}
    DRAW_FG = {'color': WHITE, 'val': 1}
    DRAW_PR_BG = {'color': RED, 'val': 2}
    DRAW_PR_FG = {'color': GREEN, 'val': 3}

    def __init__(self, image):
        self.img = image.copy()
        self.img2 = image.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)
        self.rect = (0, 0, 1, 1)
        self.drawing = False
        self.rectangle = False
        self.rect_over = False
        self.value = self.DRAW_FG
        self.thickness = 3

    def clear_drawing(self):
        # Thiết lập lại hình ảnh và mask
        self.img = self.img2.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)
        self.rect = (0, 0, 1, 1)
        self.rectangle = False
        self.rect_over = False

    def onmouse(self, event, x, y, flags):
        if event == cv2.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.rectangle:
                # Xoá hình đã vẽ trước đó
                self.clear_drawing()
                self.img = self.img2.copy()  # Khôi phục hình ảnh gốc
                cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
                self.rect = (min(self.ix, x), min(self.iy, y),
                             abs(self.ix - x), abs(self.iy - y))

        elif event == cv2.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y),
                         abs(self.ix - x), abs(self.iy - y))

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True

        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            cv2.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
            cv2.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            cv2.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
            cv2.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

    def apply_grabcut(self):
        bgdmodel = np.zeros((1, 65), np.float64)
        fgdmodel = np.zeros((1, 65), np.float64)

        if self.rect_over:  # GrabCut với hình chữ nhật
            cv2.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((self.mask == 1) | (self.mask == 3), 255, 0).astype('uint8')
        self.output = cv2.bitwise_and(self.img2, self.img2, mask=mask2)

    def reset(self):
        self.clear_drawing()

    def get_output_image(self):
        return self.output
