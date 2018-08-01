import numpy as np
import cv2
import os
import random
from getkeys import key_check
from image_preproc import preproc_img, prepare_image
from grabscreen import grab_screen
import time
from functools import reduce

data = []
data_path = "preprocessed_data_local_notshuffled_2ch\\"

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

for i in range(len(data)-1):
	img = data[i][0]
	if "Y" in key_check():
		cv2.imwrite("test.jpg", img)
		time.sleep(1)
	print(data[i][1])
	for ch in range(img.shape[2]):
		cv2.imshow("Channel {}".format(ch), cv2.resize(img[:,:,ch], (640,400), interpolation=cv2.INTERSECT_NONE))

	if cv2.waitKey(25) & 0xFF == ord('p'):
		cv2.destroyAllWindows()
		break