# train_model.py
import os
import numpy as np
from alexnet import modified_alexnet
from screen_consts import WIDTH, HEIGHT


LR = 1e-4
EPOCHS = 15
MODEL_NAME = 'wrm6-{}-{}-ep-1200K-data.model'.format('%.e'%LR,EPOCHS)
save_path = "models/"

folder = 'preprocessed_data/'

model = modified_alexnet(HEIGHT, WIDTH, 2, LR, 12)
'''if os.path.isfile(MODEL_NAME):
	model.load(MODEL_NAME)
	print("\nModel found! Continue learning.\n")
else:
	print("\nModel not found. Creating new model.\n")
'''
classes = np.zeros([12])
for i in range(EPOCHS):
	for train_data_file in os.listdir(folder):
		train_data = np.load(folder + train_data_file)

		train = train_data[:-len(train_data)//15] # 7.5% of data for test
		test = train_data[-len(train_data)//15:]

		X = np.array([i[0] for i in train]).reshape(-1, HEIGHT, WIDTH,2)
		Y = np.array([i[1] for i in train]).reshape(-1, 12)

		test_x = np.array([i[0] for i in test]).reshape(-1,HEIGHT,WIDTH,2)
		test_y = np.array([i[1] for i in test]).reshape(-1, 12)

		model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
			snapshot_step=500, show_metric=True, run_id=MODEL_NAME, shuffle=True,)
		print("\n\nACTUAL EPOCH = {}\n\n".format(i))

		model.save(save_path + MODEL_NAME)



# tensorboard --logdir=foo:D:\Python\Wormax_learn2\log