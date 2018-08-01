import random
import numpy as np
from copy import deepcopy

'''def argmin(a):
	min = a[0]
	arg = 0
	for i in range(len(a)):
		if min > a[i]:
			min = [i]
			argmin = i
	return argmin'''

def check(x,y,map):
	return x >= 0 and x < len(map) and y >= 0 and y < len(map[0])

def rec(map, x,y,d=0):
	if not check(x, y, map):
		return 1000
	if d > 6 or (map[x][y] != 0 and map[x][y] != 1):
		return 1000
	if map[x][y] == 1:
		return d
	map[x][y] = 99
	dirs = [(x,y+1),(x+1,y),(x,y-1),(x-1,y)]
	res = []
	for coord in dirs:
		if check(coord[0],coord[1],map) and (map[coord[0]][coord[1]] == 0 or map[coord[0]][coord[1]] == 1):
			res.append(rec(deepcopy(map), coord[0], coord[1],d+1))
		else:
			res.append(1000)
	return min(res)

def make_choice(x,y,field):
	actions1 = ["fire_up", "fire_down",
			"fire_left", "fire_right"]
	actions2 = ["go_up","go_right","go_down","go_left"]

	ret = [rec(deepcopy(field),x, y+1), rec(deepcopy(field),x+1,y), rec(deepcopy(field),x, y-1), rec(deepcopy(field),x-1, y)]
	#print(ret)
	act = np.argmin(ret)

	if min(ret) == 1000:
		act = random.randint(0,3)

	return actions2[act]


'''mas = [[0 for i in range(10)] for j in range(10)]
mas[1][4] = 1
pos = (5,5)

for i in range(9,-1,-1):
	for j in range(10):
		if j == pos[0] and i == pos[1]:
			print('*', end='')
		else:
			print(mas[j][i], end='')
	print()
print(make_choice(pos[0],pos[1],mas))'''