import random
from numpy import arange
import numpy as np
#from classification import *
from sklearn import metrics
from sklearn.datasets import fetch_mldata
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import time
import matplotlib.pyplot as plt

pics = np.load("my_MNIST_pics.npy")
tgts = np.load("my_MNIST_tgts.npy")

X_train = np.array(pics[:82])
y_train = np.array(tgts[:82])
X_test = np.array(pics[82:])
y_test = np.array(tgts[82:])

model = RandomForestClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
