import numpy as np
import cv2
import random
from functools import reduce
import os

data = []
data_path = "data\\data_local\\"

a = 2 / 0

listdir = []
dirsOnly = reduce(lambda x,y: x and y, map(lambda x: os.path.isdir(data_path + x), os.listdir(data_path)))
if not dirsOnly:
	listdir = filter(lambda x: os.path.isfile, os.listdir(data_path))
else:
	for dir in os.listdir(data_path):
		listdir += map(lambda x: dir + "\\" + x, os.listdir(data_path + dir))
	random.shuffle(listdir)

for file_name in listdir:
	if 1 and len(data) > 12000:
		break
	if len(data) == 0:
		data = np.load(data_path + file_name)
	else:
		data = np.concatenate((data, np.load(data_path + file_name)))


def bit_mask(img):
	ret, th1 = cv2.threshold(img, 60, 255, cv2.THRESH_TOZERO)
	return th1

# Take first frame and find corners in it
frame1 = data[0][0]
prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
	
# Create a mask image for drawing purposes
mask = np.zeros_like(frame1)

for i, frame in enumerate(data):
	frame2 = frame[0]
	next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)

	flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 3, 3, 5, 1.2, 0)

	mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
	hsv[...,0] = ang*180/np.pi/2
	hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
	rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

	cv2.imshow('frame2',cv2.resize(rgb, (640,400), interpolation=cv2.INTERSECT_NONE))
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
	elif k == ord('s'):
		cv2.imwrite('opticalfb.png',frame2)
		cv2.imwrite('opticalhsv.png',rgb)
	prvs = next

cv2.destroyAllWindows()