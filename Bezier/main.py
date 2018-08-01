import matplotlib.pyplot as plt
import numpy as np


def lerp(p1, p2, t):#return (1-t)a + tb
	return [(1-t)*p1[0], t*p2[0],(1-t)*p1[1], t*p2[1]]

def get_point(pts, t):
	a = lerp( pts[0], pts[1], t )
	b = lerp( pts[1], pts[2], t )
	c = lerp( pts[2], pts[3], t )
	d = lerp( a, b, t )
	e = lerp( b, c, t )
	return lerp( d, e, t )

pts = [[1,1],[2,-3],[5,8],[2,0]]
dots = [get_point(pts, i) for i in np.arange(0,1,0.01)]
dots = np.array(dots)

x = []
y = []
for i in dots:
	x.append(i[0])
	y.append(i[1])


plt.scatter(x,y)
plt.show()