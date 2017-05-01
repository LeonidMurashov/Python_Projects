# train_model.py

import numpy as np
from alexnet import alexnet
from screen_consts import WIDTH, HEIGHT
LR = 1e-2
EPOCHS = 20
MODEL_NAME = 'models/wormax-worm6-{}-{}-{}-epochs-120K-data.model'.format(LR, 'alexnetv2',EPOCHS)

model = alexnet(WIDTH, HEIGHT, LR)
folder = 'learn_data_colored/'
batch_size = 40

for i in range(EPOCHS):
    train_data = np.load('training_data_balanced.npy')

    train = train_data[:-(batch_size//15)*1000] # 7.5% of data
    test = train_data[-(batch_size//15)*1000:]

    X = np.array([i[0] for i in train]).reshape(-1,WIDTH,HEIGHT,1)
    Y = [i[1] for i in train]

    test_x = np.array([i[0] for i in test]).reshape(-1,WIDTH,HEIGHT,1)
    test_y = [i[1] for i in test]

    model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
        snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

    model.save(MODEL_NAME)



# tensorboard --logdir=foo:D:\Python\Wormax_learn\log





