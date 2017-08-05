import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression


def build_model(lr, batch_size):
    network = input_data(shape=[None, batch_size, 2080], name='input')
    network = fully_connected(network, 2048, activation='tanh')
    network = dropout(network, 0.5)
    network = fully_connected(network, 3, activation='tanh')
    network = regression(network, optimizer='momentum',
                         loss='mean_square',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='simple_2_lay',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')

    return model
