# balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
import cv2
import os
from screen_consts import GRAB_REGION, WIDTH, HEIGHT

folder = 'learn_data/'
arr = []
for fname in os.listdir(folder):
	if np.shape(arr) == (0,):
		arr = np.load(folder+fname)
	else:
		arr = np.concatenate((arr, np.load(folder+fname)))

print(pd.DataFrame(arr).head())



#np.random.shuffle(arr)

# Reformat data
cx = (GRAB_REGION[2] - GRAB_REGION[0])/2 + GRAB_REGION[0]
cy = (GRAB_REGION[3] - GRAB_REGION[1])/2 + GRAB_REGION[1]
kx = (GRAB_REGION[2] - GRAB_REGION[0])/2
ky = (GRAB_REGION[3] - GRAB_REGION[1])/2
for i in arr:
	#init_shape = np.shape(i[0])
	#i[0] = np.max i[0]#np.array([[min(k*2, 255) for k in j] for j in i[0]])
	#i[0].flatten()

	# Convert coordinates
	i[1][0] = (i[1][0] - cx)/kx
	i[1][1] = (i[1][1] - cy)/ky

print(pd.DataFrame(arr).head())
a = 0; b = 0
l = 0; r = 0
u = 0; d = 0
for i in arr:
	if i[1][0] < 0:
		l += 1
	else:
		r += 1
	if i[1][1] < 0:
		u += 1
	else:
		d += 1
	if i[1][2]:
		a += 1
	else:
		b += 1
print('pressed', a, ' not pressed', b)
print('left', l, ' right', r)
print('up', u, ' down', d)
print (len(arr))
np.save('training_data_balanced2.npy', arr)

for i in arr:
	cv2.imshow("name",i[0])
	print (i[1])
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
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



