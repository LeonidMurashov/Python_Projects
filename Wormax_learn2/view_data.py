import numpy as np
import cv2
import os
import random
from getkeys import key_check
from image_preproc import preproc_img
from grabscreen import grab_screen
import time
from functools import reduce
#from autoencoder_preproc import autoencode, autodecode

data = []
data_path = "data\\"

listdir = []
dirsOnly = reduce(lambda x,y: x and y, map(lambda x: os.path.isdir(data_path + x), os.listdir(data_path)))
if not dirsOnly:
	listdir = filter(lambda x: os.path.isfile, os.listdir(data_path))
else:
	for dir in os.listdir(data_path):
		listdir += map(lambda x: dir + "\\" + x, os.listdir(data_path + dir))
	random.shuffle(listdir)

for file_name in listdir:
	if 1 and len(data) > 4000:
		break
	if len(data) == 0:
		data = np.load(data_path + file_name)
	else:
		data = np.concatenate((data, np.load(data_path + file_name)))
#print("Found", len(data), "frames")

def bit_mask(img):
	ret, th1 = cv2.threshold(img, 60, 255, cv2.THRESH_TOZERO)
	return th1

def bit_mask2(img):
	kernel = np.ones((2,2),np.uint8)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	HSVLOW = np.array([0, 0, 240])
	HSVHIGH = np.array([179, 106, 255])
	mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
	mask = cv2.erode(mask,kernel, iterations=1)
	mask = cv2.dilate(mask,kernel, iterations=2)
	#res = cv2.bitwise_and(img, img, mask=mask)
	#_,res = cv2.threshold(res,1, 255, cv2.THRESH_BINARY)
	return mask

def contrast(img, clipLimit, tileGridSize):
	lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(lab)
	clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
	return clahe.apply(l)

#sh = 1000
#cv2.imshow("img1",cv2.resize(data[sh][0], (640,400), interpolation=cv2.INTERSECT_NONE))
#cv2.imshow("img2",cv2.resize(data[sh+2][0], (640,400), interpolation=cv2.INTERSECT_NONE))
#cv2.imshow("img3",cv2.resize(data[sh+4][0], (640,400), interpolation=cv2.INTERSECT_NONE))

#while True:
#	if cv2.waitKey(25) & 0xFF == ord('p'):
#			cv2.destroyAllWindows()
#			break

for i in range(len(data)-1):

	last_time = time.clock()

	img = data[i][0]#preproc_img(grab_screen((0, 125, 1000, 725)))#
	#img = cv2.imread("test.jpg")
	if "Y" in key_check():
		cv2.imwrite("test.jpg", img)
		time.sleep(1)

	if np.average(img) > 100:
		print("Too brigth frame")
		continue
	else:
		print(data[i][1])

	cv2.imshow("Original", cv2.resize(img, (640,400), interpolation=cv2.INTERSECT_NONE))
	cv2.imshow("FoodMap", cv2.resize(bit_mask2(img), (640,400), interpolation=cv2.INTERSECT_NONE))
	#cv2.imshow("autoencoded", cv2.resize(autoencode(cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)), (208,160),
	#									 interpolation=cv2.INTERSECT_NONE))
	#cv2.imshow("autodecoded", cv2.resize(autodecode(cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)), (640, 400),
	#									 interpolation=cv2.INTERSECT_NONE))
	#cv2.imshow("Grayscale", cv2.resize(cv2.cvtColor(bit_mask(img), cv2.COLOR_BGR2GRAY), (640,400), interpolation=cv2.INTERSECT_NONE))
	#cv2.imshow("HSV", cv2.resize(cv2.cvtColor(bit_mask(img), cv2.COLOR_RGB2HSV), (640,400), interpolation=cv2.INTERSECT_NONE))
	#cv2.imshow("HSV grayscale", cv2.resize(cv2.cvtColor(cv2.cvtColor(bit_mask(img), cv2.COLOR_RGB2HSV), cv2.COLOR_BGR2GRAY), (640,400), interpolation=cv2.INTERSECT_NONE))

	kernel = np.ones((2,2))
	img = bit_mask(img)
	img = contrast(img, 1, (12, 12))
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)
	cv2.imshow("Preprocessed grayscale", cv2.resize(img, (640,400), interpolation=cv2.INTERSECT_NONE))

	#time.sleep(0.06)
	if cv2.waitKey(25) & 0xFF == ord('p'):
		cv2.destroyAllWindows()
		break

	#time.sleep((time.clock() - last_time)*3.3)
	#print("Frame time:", time.clock() - last_time)
