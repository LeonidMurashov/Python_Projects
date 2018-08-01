import matplotlib.pyplot as plt
import numpy as np
from math import  factorial, cos ,pi, sin, e, tan, atan
b = 0.4
a = 3
import random
k = [ random.randrange(-50,50) for i in range(10)]

def f(x):
	y = sum([b**i*cos(a**i*pi*x) for i in range(50)])
	return y#max(-30, min(30, y))

x = np.arange(-5,5,0.0001)
y = [f(i) for i in x]
print(y)
plt.plot(x,y)
plt.show()
#