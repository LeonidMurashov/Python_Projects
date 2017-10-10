import tflearn
import tensorflow as tf
import numpy as np
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization

def modified_alexnet(width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    network = tflearn.conv_2d(network, 32, 8, strides=4, activation='relu')
    network = tflearn.conv_2d(network, 64, 4, strides=2, activation='relu')
    network = tflearn.conv_2d(network, 128, 2, strides=1, activation='relu')
    network = fully_connected(network, 512, activation='tanh')
    network = fully_connected(network, 512, activation='tanh')
    network = fully_connected(network, output, activation='tanh')
    network = regression(network, optimizer='momentum',
                         loss='mean_square',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model