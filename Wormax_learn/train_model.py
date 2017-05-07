# train_model.py
import os
import numpy as np
from alexnet import alexnet
from screen_consts import WIDTH, HEIGHT
from tensorflow.python.framework.errors import NotFoundError

LR = 5e-3
EPOCHS = 20
MODEL_NAME = 'wormax-binary-worm8-{}-{}-{}-epochs-178K-data.model'.format(LR, 'alexnetv2',EPOCHS)
save_path = "models/"

folder = 'learn_data_balanced_bool/'

model = alexnet(WIDTH, HEIGHT, LR)
'''if os.path.isfile(MODEL_NAME):
    model.load(MODEL_NAME)
    print("\nModel found! Continue learning.\n")
else:
    print("\nModel not found. Creating new model.\n")
'''
for i in range(EPOCHS):
    for train_data_file in os.listdir(folder):
        train_data = np.load(folder + train_data_file)

        train = train_data[:-len(train_data)//15] # 7.5% of data for test
        test = train_data[-len(train_data)//15:]

        X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
        Y = [i[1] for i in train]

        test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
        test_y = [i[1] for i in test]

        model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
            snapshot_step=500, show_metric=True, run_id=MODEL_NAME)
        print("\n\nACTUAL EPOCH = {}\n\n".format(i))

        model.save(save_path + MODEL_NAME)



# tensorboard --logdir=foo:D:\Python\Wormax_learn\log





