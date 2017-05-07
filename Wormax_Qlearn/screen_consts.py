import numpy as np
import cv2
WIDTH = 160
HEIGHT = 90
GRAB_REGION = (0, 125, 1000, 725)
ACTUAL_WIDTH = GRAB_REGION[2] - GRAB_REGION[0]
ACTUAL_HEIGHT = GRAB_REGION[3] - GRAB_REGION[1]
max_x = 1020; max_y = 740; min_x = 1; min_y = 109
ROI_VERTICES = [np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [WIDTH - 85, HEIGHT], [WIDTH - 85, HEIGHT - 15], [WIDTH - 105, HEIGHT - 15], [WIDTH - 105, HEIGHT], [0, HEIGHT],], np.int32)]

cx = int((GRAB_REGION[2] - GRAB_REGION[0])/2 + GRAB_REGION[0])
cy = int((GRAB_REGION[3] - GRAB_REGION[1])/2 + GRAB_REGION[1])
kx = (GRAB_REGION[2] - GRAB_REGION[0])/2
ky = (GRAB_REGION[3] - GRAB_REGION[1])/2

def roi(img, vertices):
    # blank mask:
    mask = np.zeros_like(img)
    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, (255,255,255))
    # returning the image only where mask pixels are nonzero
    masked = cv2.bitwise_and(img, mask)
    return masked