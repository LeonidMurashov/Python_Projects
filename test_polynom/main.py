import matplotlib.pyplot as plt
import numpy as np

weights = [2,1,2,7,-9,7,-8]
def f(x):
	y = np.sum([weights[i]*x**i for i in range(0,len(weights))])
	return y

x = np.arange(-5,5,0.01)
y = list(map(f, x))
print(x,y)
plt.plot(x,y)
plt.show()