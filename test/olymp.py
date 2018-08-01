points = []
for i in range(64):
	_, x, y = map(int, input().split())
	points.append([x, y])

speed = 3000
dist = 400
x, y, z = 0,0,0
time = 0

targets = int(input())
for i in range(targets+1):
	if i == targets:
		p = 0
		_z = 0
	else:
		p, _z = map(int, input().split())
		p-=1
		time += 1

	# Euclidean distance
	time += (((points[p][0] - x) * dist)**2 + ((points[p][1] - y) * dist)**2 + (_z - z)**2)**0.5 / speed
	x, y, z = points[p][0], points[p][1], _z

print(time)