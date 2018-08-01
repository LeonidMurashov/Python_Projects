import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal, getcontext
import math
import time, datetime

getcontext().prec = 40

# Color mapping
from matplotlib.cm import ScalarMappable
cmp = 'nipy_spectral'
filename = "test"
mycmap = ScalarMappable(cmap=cmp)
mycmap.to_rgba([0,1])
print(datetime.datetime.now().time())
print(filename, cmp)

class Complex:
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def __pow__(self, power, modulo=None):
		x = self.a**2-self.b**2
		self.b *= 2*self.a
		self.a = x
		return self

	def __add__(self, other):
		self.a += other.a
		self.b += other.b
		return self

	def __abs__(self):
		return self.a**2 + self.b**2

dimension = Decimal(2.5)
center = (Decimal(-0.75),Decimal(0.1))
resolution = 100
max_value = Decimal(100)
color_space = int(max_value)
drawing = 1

print(resolution, 'x', resolution)

def get_color(x,y):
	x = x/Decimal(resolution)*dimension-dimension/2 + center[0]
	y = y/Decimal(resolution)*dimension-dimension/2 + center[1]

	# Hack from Wikipedia
	p = math.sqrt((x-Decimal(0.25))**2+y**2)
	theta = math.atan2(y,x-Decimal(0.25))
	pc = 1/2 - 1/2*math.cos(theta)
	if p <= pc:
		return 1

	c = Complex(x, y)
	z = Complex(0,0)
	for i in range(color_space):
		z = z**2 + c
		if abs(z) > max_value:
			break
	return max(0, i/color_space)

from PIL import Image, ImageDraw
image = Image.new("RGB", (resolution, resolution), (0,0,0))
image_grey = Image.new("L", (resolution, resolution), (0))
draw = ImageDraw.Draw(image)
draw2 = ImageDraw.Draw(image_grey)
results = np.zeros(shape=(resolution,resolution))
for i in range(resolution):
	for j in range(resolution):
		c = get_color(i,j)
		results[i][j] = c
		clr = mycmap.to_rgba(c)
		draw2.point((i,j),(int(255*c)))
		draw.point((i, j), (int(255*clr[0]), int(255*clr[1]), int(255*clr[2])))

print('Saving')
image.save(filename+".bmp", "BMP")
image_grey.save(filename+"_grey.bmp", "BMP")
del draw, draw2
print(datetime.datetime.now().time())
if drawing:
	print('Started graphing')
	plt.gca().set_aspect('equal', adjustable='box')
	plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=1.0)
	plt.xlim([center[0].__float__()-dimension.__float__()/2, center[0].__float__()+dimension.__float__()/2])
	plt.ylim([center[1].__float__()-dimension.__float__()/2, center[1].__float__()+dimension.__float__()/2])
	plt.scatter(np.array([np.array([i] * resolution) for i in np.arange(-dimension / 2+center[0], dimension / 2+center[0], dimension / resolution)]).flatten(),
				np.array([np.array([i] * resolution) for i in np.arange(-dimension / 2+center[1], dimension / 2+center[1], dimension / resolution)]).T.flatten(),
				c=results.flatten(),marker=',', picker=True, cmap=cmp)
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