import cv2
import numpy as np

class GrabCutProcessor:
    def __init__(self, img):
        self.img = img
        self.img2 = img.copy()
        self.mask = np.zeros(img.shape[:2], np.uint8)
        self.output = np.zeros(img.shape, np.uint8)
        self.rect = (10, 10, img.shape[1] - 10, img.shape[0] - 10)
        self._run_grabcut()

    def _run_grabcut(self):
        bgdmodel = np.zeros((1, 65), np.float64)
        fgdmodel = np.zeros((1, 65), np.float64)
        cv2.grabCut(self.img2, self.mask, self.rect, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((self.mask == 1) + (self.mask == 3), 255, 0).astype('uint8')
        self.output = cv2.bitwise_and(self.img2, self.img2, mask=mask2)

    def get_output_image(self):
        return self.output
