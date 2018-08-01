import matplotlib.pyplot as plt
from random import random
from itertools import repeat
import numpy as np

n = 20
dimension = 5
center = (0,0)
resolution = 100
color_space = 20
max_value = 100


def get_color(x,y):
	x = x/resolution*dimension-dimension/2
	y = y/resolution*dimension-dimension/2
	c = x + y*1j
	z = 0
	for i in range(color_space):
		z = z**2 + c
		if abs(z) > max_value:
			break
	return i/20

results = np.zeros(shape=(resolution,resolution))
for i in range(resolution):
	for j in range(resolution):
		results[i][j] = get_color(i+center[0],j+center[1])

print('Started graphing')

#plt.scatter(list(range(resolution**2)),list(range(resolution**2)),c=results.flatten())

plt.scatter(np.array([np.array([i]*resolution) for i in range(-resolution//2,resolution//2)]).flatten(),
			np.array([np.array(list(range(-resolution//2,resolution//2)))for i in range(-resolution//2,resolution//2)]).flatten(),c=results.flatten(),marker=',')
plt.show()


'''numpy.zeros(shape=(5,2))
>>> z = 2+3j
>>> z.real
2.0
>>> z.imag
3.0
>>> z.conjugate()
(2-3j)

'''