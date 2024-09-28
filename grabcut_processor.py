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

    # Cài đặt các cờ
    rect = (0, 0, 1, 1)
    drawing = False         # Cờ cho việc vẽ
    rectangle = False       # Cờ cho việc vẽ hình chữ nhật
    rect_over = False       # Cờ kiểm tra nếu hình chữ nhật đã được vẽ
    rect_or_mask = 100      # Cờ chọn giữa hình chữ nhật và mặt nạ
    value = DRAW_FG         # Giá trị vẽ khởi tạo cho FG
    thickness = 3           # Độ dày cọ vẽ
    locked = False           # Cờ để kiểm soát việc tương tác với hình ảnh

    def __init__(self, image):
        self.img = image.copy()
        self.img2 = image.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)

    def onmouse(self, event, x, y, flags, param):
        # Nếu đang khóa không cho phép kéo ảnh
        if self.locked:
            return

        # Vẽ hình chữ nhật với chuột phải
        if event == cv2.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix, self.iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.rectangle:
                self.img = self.img2.copy()
                cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
                self.rect = (min(self.ix, x), min(self.iy, y),
                             abs(self.ix - x), abs(self.iy - y))
                self.rect_or_mask = 0

        elif event == cv2.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            cv2.rectangle(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y),
                         abs(self.ix - x), abs(self.iy - y))
            self.rect_or_mask = 0

        # Vẽ trên ảnh với chuột trái
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True

        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            cv2.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
            cv2.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False  # Kết thúc vẽ khi thả chuột trái
            cv2.circle(self.img, (x, y), self.thickness, self.value['color'], -1)
            cv2.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

    def apply_grabcut(self):
        bgdmodel = np.zeros((1, 65), np.float64)
        fgdmodel = np.zeros((1, 65), np.float64)

        if self.rect_or_mask == 0:         # GrabCut với hình chữ nhật
            cv2.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
            self.rect_or_mask = 1
        elif self.rect_or_mask == 1:       # GrabCut với mặt nạ
            cv2.grabCut(self.img2, self.mask, None, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_MASK)

        mask2 = np.where((self.mask == 1) | (self.mask == 3), 255, 0).astype('uint8')
        self.output = cv2.bitwise_and(self.img2, self.img2, mask=mask2)

    def reset(self):
        self.rect = (0, 0, 1, 1)
        self.drawing = False
        self.rectangle = False
        self.rect_or_mask = 100
        self.rect_over = False
        self.value = self.DRAW_FG
        self.img = self.img2.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.output = np.zeros(self.img.shape, np.uint8)

    def get_output_image(self):
        return self.output
