import os
import numpy as np
from neural_network import build_model
from screen_consts import WIDTH, HEIGHT
from CV_helpfile import get_rotated_samples
import random

LR = 1e-4
EPOCHS = 15
batch_size = 4
MODEL_NAME = 'wrm13-encoded-{}-{}-ep-407k-data.model'.format('%.e'%LR,EPOCHS)
save_path = "models/"

folder = 'preprocessed_encoded_notshuffled/'

model = build_model(LR, batch_size)
#model.load(save_path + MODEL_NAME)

for i in range(EPOCHS):
	listdir = os.listdir(folder)
	random.shuffle(listdir)
	for file_num, train_data_file in enumerate(listdir):
		train_data = np.load(folder + train_data_file)

		batches = [[ train_data[i2 + j2 - (batch_size-1)][0] for j2 in range(batch_size)]
												for i2 in range(len(train_data))]


		batches = np.array(batches).reshape(-1, batch_size, 2080)
		actions = np.array(train_data[:, 1].tolist()).reshape(-1, 3)

		X, Y = batches[len(train_data)//10:], actions[len(train_data)//10:]
		test_x, test_y = batches[:len(train_data)//10], actions[:len(train_data)//10]

		model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
			snapshot_step=500, show_metric=True, run_id=MODEL_NAME, shuffle=True,)
		print("\n\nepoch {}, file {}/{}\n\n".format(i+1, file_num+1, len(listdir)))

		model.save(save_path + MODEL_NAME)

# tensorboard --logdir=foo:D:\Python\Wormax_learn2\log