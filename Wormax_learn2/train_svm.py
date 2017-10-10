# train_model.py
import os
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import precision_score
from screen_consts import WIDTH, HEIGHT
from CV_helpfile import get_rotated_samples
import random
import tensorflow as tf
import pickle

LR = 1e-3
EPOCHS = 15
MODEL_NAME = 'wrm15-svm-{}-{}-ep-6M-data.model'.format(LR,EPOCHS)
save_path = "models/"
n_classes = 12

folder = 'preprocessed_data/'

'''try:
	#model = modified_alexnet(HEIGHT, WIDTH, 2, LR, n_classes)
	model.load(save_path + MODEL_NAME)
	print("Model loaded")
except:
	#model = modified_alexnet(HEIGHT, WIDTH, 2, LR, n_classes)
	print("Creating new model")
'''
model = SVC()

for i in range(EPOCHS):
	listdir = os.listdir(folder)
	random.shuffle(listdir)
	for raw_data_file in listdir:
		raw_data = np.load(folder + raw_data_file)

		# get rotated frames
		train_data_ = get_rotated_samples(raw_data, n_classes)
		#np.random.shuffle(train_data)

		# Cut by 10 parts ??
		for train_data in np.split(train_data_, np.array(np.arange(len(train_data_)//10, len(train_data_), len(train_data_)//10), np.int32)):

			train = train_data[:-len(train_data)//10] # 10% of data for test
			test = train_data[-len(train_data)//10:]

			X = np.array([i[0] for i in train]).reshape(-1, HEIGHT* WIDTH*2)
			Y = np.array([i[1] for i in train]).reshape(-1, n_classes)

			test_x = np.array([i[0] for i in test]).reshape(-1,HEIGHT*WIDTH*2)
			test_y = np.array([i[1] for i in test]).reshape(-1, n_classes)

			print(X.shape, Y.shape)

			model.fit(X,Y)
			print("Precision:",precision_score(test_y, model.predict(test_x), average='macro')  )
			print("\n\nACTUAL EPOCH = {}\n\n".format(i))

			# save the classifier
			with open(save_path + MODEL_NAME, 'wb') as fid:
				pickle.dump(model, fid)

		# load it again
		#with open('my_dumped_classifier.pkl', 'rb') as fid:
		#	gnb_loaded = pickle.load(fid)

# tensorboard --logdir=foo:D:\Python\Wormax_learn2\log