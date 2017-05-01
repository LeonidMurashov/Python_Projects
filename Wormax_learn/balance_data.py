# balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
import cv2
import os
import shutil
from screen_consts import GRAB_REGION, WIDTH, HEIGHT
import random

a = 0; b = 0
l = 0; r = 0
u = 0; d = 0

cx = (GRAB_REGION[2] - GRAB_REGION[0]) / 2 + GRAB_REGION[0]
cy = (GRAB_REGION[3] - GRAB_REGION[1]) / 2 + GRAB_REGION[1]
kx = (GRAB_REGION[2] - GRAB_REGION[0]) / 2
ky = (GRAB_REGION[3] - GRAB_REGION[1]) / 2

def balance_data(arr):
	global u,d,l,r,a,b
	# Reformat data
	for i in arr:
		if i[1][2]:	i[1][2] = 1
		else: i[1][2] = -1

		# Convert coordinates
		i[1][0] = (i[1][0] - cx)/kx
		i[1][1] = (i[1][1] - cy)/ky
	# Make statistics
	for i in arr:
		if i[1][0] < 0:	l += 1
		else: r += 1
		if i[1][1] < 0:	u += 1
		else: d += 1
		if i[1][2] > 0:	a += 1
		else: b += 1
	return arr

def main():
	dist_folder = "learn_data_balanced_colored/"
	folder = 'learn_data_colored/'
	batch_size = 40
	samples_count = 0
	arr = []

	shutil.rmtree(dist_folder)
	os.mkdir(dist_folder)

	file_names = os.listdir(folder)
	for num, fname in enumerate(file_names):
		if np.shape(arr) == (0,):
			arr = np.load(folder+fname)
		else:
			arr = np.concatenate((arr, np.load(folder+fname)))
		if (num+1) % batch_size == 0 or num+1 == len(file_names):
			balanced = balance_data(arr)
			samples_count += len(balanced)
			np.save(dist_folder + 'training_data_balanced-{}.npy'.format(num//batch_size), balanced)
			print(dist_folder +  'training_data_balanced-{}.npy was saved'.format(num//batch_size))
			del balanced
			if not num+1 == len(file_names): arr = []

	print(pd.DataFrame(arr).head())
	print('pressed', a, ' not pressed', b)
	print('left', l, ' right', r)
	print('up', u, ' down', d)
	print (samples_count)

main()


# show data
'''for i in range(random.randint(0,len(arr)-1000), len(arr)):
	cv2.imshow("name",arr[i][0])
	print (arr[i][1])
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break'''
'''

lefts = []
rights = []
forwards = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]

    if choice == [1,0,0]:
        lefts.append([img,choice])
    elif choice == [0,1,0]:
        forwards.append([img,choice])
    elif choice == [0,0,1]:
        rights.append([img,choice])
    else:
        print('no matches')


forwards = forwards[:len(lefts)][:len(rights)]
lefts = lefts[:len(forwards)]
rights = rights[:len(forwards)]

final_data = forwards + lefts + rights
shuffle(final_data)

np.save('training_data.npy', final_data)
'''



