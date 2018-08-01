import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal, getcontext
getcontext().prec = 20





#### THIS DO NOT WORK











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

dimension = Decimal(3)
center = [Decimal(-1),Decimal(0)]
resolution = 100
max_value = Decimal(20)
color_space = int(max_value)

def get_color(x,y):
	x = x/Decimal(resolution)*dimension-dimension/2 + center[0]
	y = y/Decimal(resolution)*dimension-dimension/2 + center[1]
	c = Complex(x, y)
	z = Complex(0,0)
	for i in range(color_space):
		z = z**2 + c
		if abs(z) > max_value:
			break
	return i/color_space

results = np.zeros(shape=(resolution,resolution))
for i in range(resolution):
	for j in range(resolution):
		results[i][j] = get_color(i,j)

print('Started graphing')

fig = plt.figure()
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=1.0)
plt.xlim([center[0].__float__()-dimension.__float__()/2, center[0].__float__()+dimension.__float__()/2])
plt.ylim([center[1].__float__()-dimension.__float__()/2, center[1].__float__()+dimension.__float__()/2])
scatter = plt.scatter(np.array([np.array([i] * resolution) for i in np.arange(-dimension / 2+center[0], dimension / 2+center[0], dimension / resolution)]).flatten(),
			np.array([np.array([i] * resolution) for i in np.arange(-dimension / 2+center[1], dimension / 2+center[1], dimension / resolution)]).T.flatten(),
			c=results.flatten(),marker=',', picker=True)

px, py = 0, 0
def onMouseEvent(event):
	global px, py, center, dimension
	x, y, axes, name, button = event.xdata, event.ydata, event.inaxes, event.name, event.button
	if button != 1:
		return
	print(x,y,axes)
	if name == 'button_release_event':
		print(axes.get_xlim())
		center[0] -= Decimal(x) - Decimal(px)
		center[1] -= Decimal(y) - Decimal(py)
		dimension = Decimal(axes.get_xlim()[1] - axes.get_xlim()[1])

		for i in range(resolution):
			for j in range(resolution):
				results[i][j] = get_color(i, j)

		fig.canvas.draw_idle()
		fig.canvas.draw()
		fig.canvas.flush_events()


	if name == 'button_press_event':
		px = x
		py = y
		pass


button_press_event_id = fig.canvas.mpl_connect('button_press_event', onMouseEvent)
button_release_event_id = fig.canvas.mpl_connect('button_release_event', onMouseEvent)
plt.show()

# Отпишемся от событий
fig.canvas.mpl_disconnect(button_press_event_id)
fig.canvas.mpl_disconnect(button_release_event_id)


'''numpy.zeros(shape=(5,2))
>>> z = 2+3j
>>> z.real
2.0
>>> z.imag
3.0
>>> z.conjugate()
(2-3j)

'''