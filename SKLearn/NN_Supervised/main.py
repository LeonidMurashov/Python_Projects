import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                       hidden_layer_sizes=(5, 2), random_state=1)
#clf = svm.SVC(gamma=0.0001, C=100)

print(len(digits.data))

x, y = digits.data[:-10], digits.target[:-10]
clf.fit(x, y)

for i in range(10):
	print('Prediction:', clf.predict(digits.data[-(i+1)]))
	plt.imshow(digits.images[-(i+1)], cmap=plt.cm.gray_r, interpolation="nearest")
	plt.show()
