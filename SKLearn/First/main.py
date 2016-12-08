import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

clf = svm.SVC(gamma=0.0001, C=100)

print(len(digits.data))

x, y = digits.data[:-10], digits.target[:-10]
clf.fit(x, y)

for i in range(100):
	print('Prediction:', clf.predict(digits.data[i+10]))
	plt.imshow(digits.images[i+10], cmap=plt.cm.gray_r, interpolation="nearest")
	plt.show()
