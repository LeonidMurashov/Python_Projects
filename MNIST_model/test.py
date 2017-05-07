import numpy
import random
from numpy import arange
import numpy as np
#from classification import *
from sklearn import metrics, datasets, svm
from sklearn.datasets import fetch_mldata
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import time
import _pickle as cPickle
import matplotlib.pyplot as plt
from PIL import Image

def run():
	digits = datasets.load_digits()
	pics = np.load("my_MNIST_pics.npy")
	tgts =  np.load("my_MNIST_tgts.npy")

	#mnist.data, mnist.target = shuffle(mnist.data, mnist.target)
	#print mnist.data.shape
	# Trunk the data
	n_train = int(len(pics)*0.5)
	n_test = int(len(pics)*0.5)
	# Define training and testing sets
	indices = arange(len(pics))
	#train_idx = random.sample(indices, n_train)
	#test_idx = random.sample(indices, n_test)
	train_idx = arange(0,n_train)
	test_idx = arange(n_train+1,n_train+n_test)

	X_train, y_train = pics[train_idx], tgts[train_idx]
	X_test, y_test = pics[test_idx], tgts[test_idx]

	# Apply a learning algorithm
	print ("Applying a learning algorithm...")
	clf = svm.SVC(gamma=0.01)#RandomForestClassifier(n_estimators=11,n_jobs=2)
	#print(X_train[0], '\n\n', y_train[0])

	'''while 1:
		i = random.randint(0,70)
		print(y_train[i])
		plt.imshow(X_train[i], cmap=plt.cm.gray_r, interpolation='nearest')
		plt.show()'''

	clf.fit(X_train, y_train)

	# Make a prediction
	print ("Making predictions...")
	y_pred = clf.predict(X_test)

	#print y_pred

	# Evaluate the prediction
	print ("Evaluating results...")
	print ("Precision: \t", metrics.precision_score(y_test, y_pred, average="weighted"))
	print ("Recall: \t", metrics.recall_score(y_test, y_pred, average="weighted"))
	print ("F1 score: \t", metrics.f1_score(y_test, y_pred, average="weighted"))
	print ("Mean accuracy: \t", clf.score(X_test, y_test))

	# save the classifier
	with open('my_dumped_classifier.pkl', 'wb') as fid:
		cPickle.dump(clf, fid)

	# load it again
	with open('my_dumped_classifier.pkl', 'rb') as fid:
		gnb_loaded = cPickle.load(fid)

		while 1:
			i = random.randint(0,len(X_test))
			print("act:",y_test[i], "prec:", gnb_loaded.predict(X_test[i]))
			plt.imshow(np.reshape(X_test[i], [20,10]), cmap=plt.cm.gray_r, interpolation='nearest')
			plt.show()


if __name__ == "__main__":
	start_time = time.time()
	results = run()
	end_time = time.time()
	print ("Overall running time:", end_time - start_time)