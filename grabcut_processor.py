import cv2 as cv
import numpy as np

# Constants for the mask drawing values
DRAW_BG = {'color': [0, 0, 0], 'val': 0}       # Definite Background
DRAW_FG = {'color': [255, 255, 255], 'val': 1}  # Definite Foreground
DRAW_PR_BG = {'color': [128, 128, 128], 'val': 2}  # Probable Background
DRAW_PR_FG = {'color': [192, 192, 192], 'val': 3}  # Probable Foreground

class GrabCutProcessor:
    def __init__(self, img):
        self.img = img
        self.img_copy = img.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)  # Initial mask
        self.rect = (0, 0, 1, 1)
        self.bgd_model = np.zeros((1, 65), np.float64)
        self.fgd_model = np.zeros((1, 65), np.float64)
        self.rect_or_mask = 0  # Indicates if we are using rectangle or mask
        self.drawing = False
        self.value = DRAW_FG  # Default to drawing foreground
        self.thickness = 3
        self.ix, self.iy = -1, -1  # For drawing rectangle

    def set_drawing_value(self, val):
        """ Set the value to draw either background, foreground, probable background, or probable foreground """
        if val == 0:
            self.value = DRAW_BG
        elif val == 1:
            self.value = DRAW_FG
        elif val == 2:
            self.value = DRAW_PR_BG
        elif val == 3:
            self.value = DRAW_PR_FG

    def apply_grabcut(self, rect=None):
        """ Apply the GrabCut algorithm using the rect or mask """
        if rect:
            self.rect = rect
            cv.grabCut(self.img_copy, self.mask, self.rect, self.bgd_model, self.fgd_model, 5, cv.GC_INIT_WITH_RECT)
            self.rect_or_mask = 1  # Now we are using the mask
        else:
            cv.grabCut(self.img_copy, self.mask, self.rect, self.bgd_model, self.fgd_model, 5, cv.GC_INIT_WITH_MASK)

        mask2 = np.where((self.mask == 1) + (self.mask == 3), 255, 0).astype('uint8')
        output = cv.bitwise_and(self.img_copy, self.img_copy, mask=mask2)
        return output

    def update_mask(self, x, y, event_type):
        """ Update the mask with the current drawing value """
        if event_type == 'mousedown':
            self.drawing = True
            self.ix, self.iy = x, y
        elif event_type == 'mousemove' and self.drawing:
            cv.circle(self.img_copy, (x, y), self.thickness, self.value['color'], -1)
            cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)
        elif event_type == 'mouseup':
            self.drawing = False
            cv.circle(self.img_copy, (x, y), self.thickness, self.value['color'], -1)
            cv.circle(self.mask, (x, y), self.thickness, self.value['val'], -1)

    def reset(self):
        """ Reset the image and mask """
        self.img_copy = self.img.copy()
        self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
        self.rect_or_mask = 0
        return self.img_copy
