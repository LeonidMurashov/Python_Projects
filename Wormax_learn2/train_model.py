# train_model.py
import os
import numpy as np
from alexnet_easy import modified_alexnet
from screen_consts import WIDTH, HEIGHT
from CV_helpfile import get_rotated_samples
import random

LR = 1e-3
uiui = 1e-3
EPOCHS = 15
MODEL_NAME = 'wrm10-easy-{}-{}-ep-6M-data.model'.format('%.e'%uiui,EPOCHS)
save_path = "models/"
n_classes = 12

folder = 'preprocessed_data/'

model = modified_alexnet(HEIGHT, WIDTH, 2, LR, n_classes)
try:
	#model = modified_alexnet(HEIGHT, WIDTH, 2, LR, n_classes)
	model.load(save_path + MODEL_NAME)
	print("Model loaded")
except:
	#model = modified_alexnet(HEIGHT, WIDTH, 2, LR, n_classes)
	print("Cannot load model")


for i in range(EPOCHS):
	listdir = os.listdir(folder)
	random.shuffle(listdir)
	for raw_data_file in listdir:
		raw_data = np.load(folder + raw_data_file)

		# get rotated frame s
		train_data_ = get_rotated_samples(raw_data, n_classes)
		np.random.shuffle(train_data_)

		for train_data in np.split(train_data_, np.array(np.arange(len(train_data_)//10, len(train_data_), len(train_data_)//10), np.int32)):

			train = train_data[:-len(train_data)//10] # 10% of data for test
			test = train_data[-len(train_data)//10:]

			X = np.array([i[0] for i in train]).reshape(-1, HEIGHT, WIDTH,2)
			Y = np.array([i[1] for i in train]).reshape(-1, n_classes)

			test_x = np.array([i[0] for i in test]).reshape(-1,HEIGHT,WIDTH,2)
			test_y = np.array([i[1] for i in test]).reshape(-1, n_classes)

			model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
				snapshot_step=500, show_metric=True, run_id=MODEL_NAME, shuffle=True,)
			print("\n\nACTUAL EPOCH = {}\n\n".format(i))

			model.save(save_path + MODEL_NAME)

# tensorboard --logdir=foo:D:\Python\Wormax_learn2\log