import tflearn
import numpy as np

def build_m1():
	model = tflearn.input_data([None,1])
	model = tflearn.fully_connected(model, 1)
	model = tflearn.regression(model)
	model = tflearn.DNN(model)
	return model

model1 = build_m1()
model1.load("./foo1.model")
