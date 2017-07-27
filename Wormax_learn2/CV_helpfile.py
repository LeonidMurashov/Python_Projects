from itertools import groupby

import cv2
import numpy as np
from image_preproc import bit_mask2, roi_gray, bit_mask3, bit_mask, contrast
from screen_consts import HEIGHT, WIDTH, get_direction
import matplotlib.pyplot as plt
from functools import reduce
import os
import random
import time
from grabscreen import grab_screen
from getkeys import key_check


def detect_any_worms(original, food_map=None):
	img = original
	kernel = np.ones((2, 2))
	kernel2 = np.ones((3, 3))
	img = cv2.medianBlur(img, 3)
	img = bit_mask3(img)
	w1, h1 = 10, 25
	w2, h2, = 40, 25
	img = roi_gray(img, [np.array(
		[[w1, 0], [WIDTH - w2, 0], [WIDTH - w2, h2], [WIDTH, h2], [WIDTH, HEIGHT], [0, HEIGHT], [0, h1], [w1, h1]],
		np.int32)])
	img = cv2.erode(img, kernel, iterations=1)
	img = cv2.dilate(img, kernel, iterations=3)
	img = cv2.erode(img, kernel, iterations=1)

	ret, img = cv2.threshold(img, 4, 255, 0)
	im2, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	#cv2.imshow("Or;iginal", cv2.resize(im2, (640, 400), interpolation=cv2.INTERSECT_NONE))
	if hierarchy is not None and len(hierarchy) > 0:
		if food_map is not None:
			any_food = cv2.mean(food_map)[0] > 0
		else:
			any_food = cv2.mean(bit_mask2(original))[0] > 0
		return len(hierarchy[0]) > 1 or any_food
	return 0


def get_one_hot(x, y, n_classes):
	one_hot = np.zeros([n_classes])
	one_hot[get_direction(x, y, n_classes)] = 1
	return one_hot

def rotated_frames(img, x, y, n_classes):
	flip = cv2.flip(img, 0)
	return [[img, get_one_hot(x, y, n_classes)],
			[flip, get_one_hot(x, -y, n_classes)],
			[cv2.flip(img, 1), get_one_hot(-x, y, n_classes)],
			[cv2.flip(flip, 1), get_one_hot(-x, -y, n_classes)]]


def rotated_frames2(img, x, y, n_classes):
	rows, cols = len(img),len(img[0])
	rot_M_vec = [cv2.getRotationMatrix2D((0, 0), i, 1)[:, :2] for i in np.arange(0, 360, 360 / n_classes)]
	rot_M_img = [cv2.getRotationMatrix2D((cols/2, rows/2), i, 1) for i in np.arange(0, 360, 360 / n_classes)]
	vec = np.array([x, y]).T

	#M = cv2.getRotationMatrix2D((cols/2 ,rows/2), angle, 1)
	#dst = #[0:cols, 0:rows]
	return [[cv2.warpAffine(img, rot_M_img[i], (cols, rows)), np.dot(rot_M_vec[i], vec,)] for i in range(n_classes)]

def get_rotated_samples(samples, n_classes):
	final_samples = []
	for i in samples:
		rotated = rotated_frames2(i[0], i[1][0], i[1][1], n_classes)
		for j in range(len(rotated)):
			rotated[j][1] = list(get_one_hot(rotated[j][1][0], rotated[j][1][1], n_classes))
			#rotated[j][1].append(i[1][2])
		final_samples.append(rotated)
	return np.concatenate(final_samples)


#arr = np.array(rotated_frames2(grab_screen(),0,1,12))
'''for i in arr[:,1,]:
	print(i)
plt.scatter(arr[:,1,:1],arr[:,1,1:])
plt.show()
#dst = cv2.warpAffine(img, M, (cols, rows))  # [0:cols, 0:rows]'''

'''
data = []
data_path = "data\\data_local\\"

listdir = []
dirsOnly = reduce(lambda x,y: x and y, map(lambda x: os.path.isdir(data_path + x), os.listdir(data_path)))
if not dirsOnly:
	listdir = list(filter(lambda x: os.path.isfile, os.listdir(data_path)))
else:
	for dir in os.listdir(data_path):
		listdir += map(lambda x: dir + "\\" + x, os.listdir(data_path + dir))
random.shuffle(listdir)

for file_name in listdir:
	if len(data) > 10000:
		break
	if len(data) == 0:
		data = np.load(data_path + file_name)
	else:
		data = np.concatenate((data, np.load(data_path + file_name)))
np.random.seed(100000)
np.random.shuffle(data)
r = random.randint(0, len(data)-2000)
for j,frame in enumerate(data[r:]):
	if j%10 == 0:
		img = frame[0]
		kernel = np.ones((2,2))
		img = bit_mask(img)
		img = contrast(img, 1, (12, 12))
		img = cv2.dilate(img, kernel, iterations=1)
		img = cv2.erode(img, kernel, iterations=1)
		#img = cv2.resize(grab_screen(),(1280,720))
		for _,i in enumerate(rotated_frames2(img, frame[1][0], frame[1][1], 12)):
			cv2.imshow(";", cv2.resize(i[0], (640, 400), interpolation=cv2.INTERSECT_NONE))
			print(str(get_one_hot(i[1][0], i[1][1], n_classes=12)))
			time.sleep(1)
			#cv2.imshow("f",img)
			if cv2.waitKey(25) & 0xFF == ord('p'):
				cv2.destroyAllWindows()
				time.sleep(0.001)
				break'''

'''data = []
data_path = "data\\data_local\\"

listdir = []
dirsOnly = reduce(lambda x,y: x and y, map(lambda x: os.path.isdir(data_path + x), os.listdir(data_path)))
if not dirsOnly:
	listdir = filter(lambda x: os.path.isfile, os.listdir(data_path))
else:
	for dir in os.listdir(data_path):
		listdir += map(lambda x: dir + "\\" + x, os.listdir(data_path + dir))
	random.shuffle(listdir)

for file_name in listdir:
	if len(data) > 10000:
		break
	if len(data) == 0:
		data = np.load(data_path + file_name)
	else:
		data = np.concatenate((data, np.load(data_path + file_name)))
np.random.seed(100000)
np.random.shuffle(data)

for frame in data[random.randint(0,len(data)-1000):len(data)]:
	img = frame[0]
	food_map = bit_mask2(img)

	cv2.imshow("Original", cv2.resize(img, (640, 400), interpolation=cv2.INTERSECT_NONE))
	cv2.imshow("food", cv2.resize(food_map, (640, 400), interpolation=cv2.INTERSECT_NONE))

	if detect_any_worms(img, food_map):
		print("No worms", "".join(["!" for i in range(random.randint(1, 5))]))

		while True:
			if cv2.waitKey(25) & 0xFF == ord('p'):
				cv2.destroyAllWindows()
				time.sleep(0.01)
				break'''
'''gray = cv2.circle(img, (120, 120), 20, (100, 200, 80), -1)
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
							   param1=30,
							   param2=15,
							   minRadius=0,
							   maxRadius=0)

	if circles != None and len(circles) > 0:
		for i in circles[0, :]:
			cv2.circle(img, (i[0], i[1]), i[2], (255, 255, 255), 2)
			cv2.circle(img, (i[0], i[1]), 2, (255, 255, 255), 3)

'''

'''
	img = np.zeros_like(img)
	if corners != None and len(corners) > 0:
		for i in corners:
			cv2.circle(img, (i[0], i[1]), 3, (255, 255, 255), 2)
'''
	#cv2.imshow('corners', cv2.resize(im2, (640,400), interpolation=cv2.INTERSECT_NONE))
