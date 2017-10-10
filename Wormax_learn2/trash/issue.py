import tflearn
import tensorflow as tf

def build_m1():
	model = tflearn.input_data([None,3,3,1])
	model = tflearn.conv_2d(model,1,3)
	model = tflearn.fully_connected(model, 10)
	model = tflearn.regression(model)
	model = tflearn.DNN(model)
	return model

def build_m2():
	model = tflearn.input_data([None,3])
	model = tflearn.fully_connected(model, 10)
	model = tflearn.regression(model)
	model = tflearn.DNN(model)
	return model

model1 = build_m1()
model2 = build_m2()

model1.save("foo1")
model2.save("foo2")

del model1, model2
tf.reset_default_graph()
model1 = build_m1()
model2 = build_m2()
model1.load("foo1")
model2.load("foo2")
