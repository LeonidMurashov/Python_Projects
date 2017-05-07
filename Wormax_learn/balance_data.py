# balance_data.py

import numpy as np
import pandas as pd
import random
import cv2
import os
import shutil
from screen_consts import GRAB_REGION, WIDTH, HEIGHT
from CV_helpfile import bit_mask, detect_lose
import copy

a = 0; b = 0
l = 0; r = 0
u = 0; d = 0
deleted = 0

cx = (GRAB_REGION[2] - GRAB_REGION[0]) / 2 + GRAB_REGION[0]
cy = (GRAB_REGION[3] - GRAB_REGION[1]) / 2 + GRAB_REGION[1]
kx = (GRAB_REGION[2] - GRAB_REGION[0]) / 2
ky = (GRAB_REGION[3] - GRAB_REGION[1]) / 2

def balance_data(arr):
	global u,d,l,r,a,b,loses,deleted
	# Reformat data
	for num, i in enumerate(arr):
		if i[1][2]:	i[1][2] = 1
		else: i[1][2] = -1
		# Convert coordinates
		i[1][0] = (i[1][0] - cx)/kx
		i[1][1] = (i[1][1] - cy)/ky

		if num % 4 == 0: # Check every 6 frames
			if detect_lose(i[0]):
				arr[num][1] = "marked" # Mark prev 100 frames

		# Make image binary
		i[0] = bit_mask(i[0])
	arr = list(arr)
	for i in range(len(arr))[::-1]:
		try:
			if arr[i][1] == "marked":
				for j in range(100):
					arr = arr[:i-j] + arr[i-j+1:]
					#np.delete(arr, i-j)
					'''for k in range(len(arr[i - j][0])):
						for h in range(len(arr[i - j][0][k])):
							arr[i-j][0][k][h] = 128
							arr[i - j][1] = [1,1,1]'''
					deleted+=1
		except:
			pass

	# Make statistics
	for i in arr:
		if i[1][0] < 0:	l += 1
		else: r += 1
		if i[1][1] < 0:	u += 1
		else: d += 1
		if i[1][2] > 0:	a += 1
		else: b += 1
		np.random.shuffle(arr)
	return arr

def main():
	dist_folder = "learn_data_balanced_bool/"
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
			balanced = balance_data(copy.deepcopy(arr))
			samples_count += len(balanced)
			np.save(dist_folder + 'training_data_balanced-{}.npy'.format(num//batch_size), balanced)
			print(dist_folder +  'training_data_balanced-{}.npy was saved'.format(num//batch_size))
			arr = []

			#for i in range(random.randint(0, len(balanced) - 1000), len(balanced)):
				#cv2.imshow("name", balanced[i][0])
				#print(arr[i][1])
				#if cv2.waitKey(25) & 0xFF == ord('q'):
				#	cv2.destroyAllWindows()
				#	break
			del balanced

	print(pd.DataFrame(arr).head())
	print('pressed', a, ' not pressed', b)
	print('left', l, ' right', r)
	print('up', u, ' down', d)
	print('loses', deleted//100, ' deleted', deleted)
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



