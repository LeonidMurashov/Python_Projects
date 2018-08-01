# train_model.py
import os
import numpy as np
from alexnet_easy import modified_alexnet
from screen_consts import WIDTH, HEIGHT
from CV_helpfile import get_rotated_samples
import random
import tensorflow as tf
import cv2
import numpy as np

LR = 1e-3
EPOCHS = 15
MODEL_NAME = 'wrm24-sequence-{}-{}-ep-0.5M-data.model'.format(LR,EPOCHS)
save_path = "models/"
n_classes = 12
frames = 6

folder = 'preprocessed_data/'

'''try:
	#model = modified_alexnet(HEIGHT, WIDTH, 2, LR, n_classes)
	
	print("Model loaded")
except:
	#model = modified_alexnet(HEIGHT, WIDTH, 2, LR, n_classes)
	print("Creating new model")
'''
model = modified_alexnet(HEIGHT, WIDTH, 2, frames, LR, n_classes)
#model.load(save_path + MODEL_NAME)

for i in range(EPOCHS):
	listdir = os.listdir(folder)
	random.shuffle(listdir)
	for raw_data_file in listdir:
		raw_data = np.load(folder + raw_data_file)

		# get rotated frames
		train_data_ = get_rotated_samples(raw_data, n_classes)
		#print(train_data_[0][1])
		np.random.shuffle(train_data_)
		# Cut by 10 parts ??
		for train_data in np.split(train_data_, np.array(np.arange(len(train_data_)//10, len(train_data_), len(train_data_)//10), np.int32)):

			train_data_series = [train_data[j:j+frames] for j in range(len(train_data) - frames)]
			train_data = []
			for it in range(len(train_data_series)-1):
				train_data_sample = []
				aa = np.array([ np.transpose(cv2.split(np.array(fr[0])),(1,2,0)) for fr in train_data_series[it]])
				aa = cv2.merge(aa)
				train_data_sample.append(aa)
				train_data_sample.append(train_data_series[it][frames-1][1])
				train_data.append(train_data_sample)

			train_data = np.array(train_data)
			np.random.shuffle(train_data)

			train = train_data[:-len(train_data)//10] # 10% of data for test
			test = train_data[-len(train_data)//10:]

			X = np.array([i[0] for i in train]).reshape(-1, HEIGHT, WIDTH,frames*2)
			Y = np.array([i[1] for i in train]).reshape(-1, n_classes)

			test_x = np.array([i[0] for i in test]).reshape(-1,HEIGHT,WIDTH,frames*2)
			test_y = np.array([i[1] for i in test]).reshape(-1, n_classes)

			#print(test_y[0])

			model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
				snapshot_step=500, show_metric=True, run_id=MODEL_NAME, shuffle=True,)

			print(model.predict(np.array(test_x[0]).reshape(-1,HEIGHT,WIDTH,frames*2)))
			print("\n\nACTUAL EPOCH = {}\n\n".format(i))

			model.save(save_path + MODEL_NAME)

# tensorboard --logdir=foo:D:\Python\Wormax_learn2\log