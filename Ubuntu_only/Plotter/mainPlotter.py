#https://www.youtube.com/watch?v=ZmYPzESC5YY&list=PLQVvvaa0QuDfefDfXb9Yf0la1fPDKluPF&index=16
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
from matplotlib import style

style.use('fivethirtyeight')

inputfile1 = sys.argv[1]
inputfile2 = sys.argv[2]
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ax2 = fig.add_subplot(1, 1, 1)

prevX1 = prevY1 = []
prevX2 = prevY2 = []

def animate(i):
	global prevY1, prevX1, prevX2, prevY2
	x1, y1 = np.loadtxt(inputfile1, delimiter=';', unpack=True)
	x2, y2 = np.loadtxt(inputfile2, delimiter=';', unpack=True)
	if not (np.all(x2 == prevX2) and np.all(y2 == prevY2)) or not (np.all(x1 == prevX1) and np.all(y1 == prevY1)):
		ax1.clear()
		ax2.clear()
		ax1.plot(x1, y1)
		prevX1 = x1
		prevY1 = y1

		ax2.plot(x2, y2)
		prevX2 = x2
		prevY2 = y2
ani = animation.FuncAnimation(fig, animate, interval=200)
plt.show()

