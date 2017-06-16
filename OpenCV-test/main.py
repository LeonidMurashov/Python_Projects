import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = 'left3.bmp'
img2 = 'right3.bmp'

imgL = cv2.resize(cv2.imread(img1,0), (500,400))
imgR = cv2.resize(cv2.imread(img2,0), (500,400))

#imgL = cv2.imread(img1,0)
#imgR = cv2.imread(img2,0)



stereo = cv2.StereoBM_create(numDisparities=0, blockSize=27)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
cv2.imshow("name",imgL)
plt.show()