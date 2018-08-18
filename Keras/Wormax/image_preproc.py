import numpy as np
import cv2
from screen_consts import target_resolution, WIDTH, HEIGHT

def roi(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, [255,255,255])
	masked = cv2.bitwise_and(img, mask)
	return masked

def roi_gray(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, 255)
	masked = cv2.bitwise_and(img, mask)
	return masked

def preproc_img(img):
	#img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	k = target_resolution[0]/len(img[0])
	img = cv2.resize(img, (int(len(img[0])*k), int(len(img)*k)))
	img = img[(len(img)-target_resolution[1])//2:(len(img)-target_resolution[1])//2+target_resolution[1], :]

	img = cv2.resize(img, (WIDTH, HEIGHT))
	cover_rect = (30,20)
	img = roi(img, [np.array([[0,0], [WIDTH, 0], [WIDTH,HEIGHT],
							[WIDTH//2+cover_rect[0]//2, HEIGHT],
							[WIDTH//2+cover_rect[0]//2, HEIGHT-cover_rect[1]//2],
							[WIDTH//2-cover_rect[0]//2, HEIGHT-cover_rect[1]//2],
							[WIDTH//2-cover_rect[0]//2, HEIGHT],
							[0,HEIGHT]], np.int32)])
	return img

def get_preprocessed_and_map(img):
	return preproc_img(img), cv2.resize(img[905:1050-13, 1535:1680-13,1],(33,33))

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
	res = cv2.bitwise_and(img, img, mask=mask)
	res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
	_,res = cv2.threshold(res,1, 255, cv2.THRESH_BINARY)
	return res

def bit_mask3(img):
	kernel = np.ones((2,2),np.uint8)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	HSVLOW = np.array([0, 0, 110])
	HSVHIGH = np.array([179, 255, 255])
	mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
	res = cv2.bitwise_and(img, img, mask=mask)
	res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
	_,res = cv2.threshold(res,1, 255, cv2.THRESH_BINARY)
	return res

def contrast(img, clipLimit, tileGridSize):
	lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	l, a, b = cv2.split(lab)
	clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
	return clahe.apply(l)

def prepare_image(img, return_food=False):
	food_img = bit_mask2(img)
	kernel = np.ones((2,2))
	img = bit_mask(img)
	img = contrast(img, 1, (12, 12))
	img = cv2.dilate(img, kernel, iterations=1)
	img = cv2.erode(img, kernel, iterations=1)
	gray_img = img

	merged = np.array(cv2.merge([gray_img, food_img]))
	if return_food:
		return merged, food_img
	else:
		return merged