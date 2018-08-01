import tflearn
import tensorflow as tf
import numpy as np
from tflearn import embedding
from tflearn import lstm
from tflearn import merge
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
def modified_alexnet(width, height, channels, frames, lr, output=3):
    network = input_data(shape=[None, width, height, channels*frames], name='input')
    print(network.shape)
    network = tflearn.conv_2d(network, 32, 16, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 64, 8, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 8, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 4, strides=1, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 4, strides=1, activation='relu')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, output, activation='softmax')
    print(network.shape)
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model


'''
worm 22

def modified_alexnet(width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    print(network.shape)
    network = tflearn.conv_2d(network, 32, 16, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 64, 8, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 8, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 256, 4, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 512, 4, strides=1, activation='relu')
    print(network.shape)
    network = fully_connected(network, 1024, activation='tanh')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, output, activation='softmax')
    print(network.shape)
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model

'''

'''
worm 21

def modified_alexnet(width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    print(network.shape)
    network = conv_2d(network, 96, 11, strides=4, activation='relu')
    print(network.shape)
    network = max_pool_2d(network, 3, strides=2)
    print(network.shape)
    network = local_response_normalization(network)
    print(network.shape)
    network = conv_2d(network, 256, 5, activation='relu')
    print(network.shape)
    network = max_pool_2d(network, 3, strides=2)
    print(network.shape)
    network = local_response_normalization(network)
    print(network.shape)
    network = conv_2d(network, 384, 3, activation='relu')
    print(network.shape)
    network = conv_2d(network, 384, 3, activation='relu')
    print(network.shape)
    network = conv_2d(network, 256, 3, activation='relu')
    print(network.shape)
    network = max_pool_2d(network, 3, strides=2)
    print(network.shape)
    network = local_response_normalization(network)
    print(network.shape)
    network = fully_connected(network, 4096, activation='tanh')
    print(network.shape)
    network = dropout(network, 0.5)
    print(network.shape)
    network = fully_connected(network, 4096, activation='tanh')
    print(network.shape)
    network = dropout(network, 0.5)
    print(network.shape)
    network = fully_connected(network, output, activation='softmax')
    print(network.shape)
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model

'''


'''
worm20

def modified_alexnet(width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    print(network.shape)
    network = tflearn.conv_2d(network, 32, 16, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 64, 8, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 8, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 4, strides=1, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 4, strides=1, activation='relu')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, output, activation='softmax')
    print(network.shape)
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model

'''

'''
worm 19

def modified_alexnet(width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    print(network.shape)
    network = tflearn.conv_2d(network, 32, 8, strides=4, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 64, 4, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 2, strides=1, activation='relu')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, output, activation='softmax')
    print(network.shape)
    network = regression(network, optimizer='adadelta',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model


'''


'''
worm18

def modified_alexnet(width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    print(network.shape)
    network = tflearn.conv_2d(network, 32, 8, strides=4, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 64, 4, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 2, strides=1, activation='relu')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, output, activation='softmax')
    print(network.shape)
    network = regression(network, optimizer='nesterov',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model

'''


'''
worm17

def modified_alexnet(width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    print(network.shape)
    network = tflearn.conv_2d(network, 32, 8, strides=4, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 64, 4, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 2, strides=1, activation='relu')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, output, activation='softmax')
    print(network.shape)
    network = regression(network, optimizer='adam',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model

'''

'''
worm16

def modified_alexnet(width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    print(network.shape)
    network = tflearn.conv_2d(network, 32, 8, strides=4, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 64, 4, strides=2, activation='relu')
    print(network.shape)
    network = tflearn.conv_2d(network, 128, 2, strides=1, activation='relu')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, 512, activation='tanh')
    print(network.shape)
    network = fully_connected(network, output, activation='softmax')
    print(network.shape)
    network = regression(network, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model_alexnet',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model

'''

#modified_alexnet(160, 100, 2, 0.001)
'''
worm 14
rotated frames
lighted grey and food channels
shuffled

(?, 160, 100, 2)
(?, 40, 25, 32)
(?, 20, 13, 64)
(?, 20, 13, 128)
(?, 512)
(?, 512)
(?, 3)

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

'''

'''
worm 23

def modified_alexnet( width, height, channels, lr, output=3):
    network = input_data(shape=[None, width, height, channels], name='input')
    conv1_7_7 = conv_2d(network, 64, 7, strides=2, activation='relu', name='conv1_7_7_s2')
    pool1_3_3 = max_pool_2d(conv1_7_7, 3, strides=2)
    pool1_3_3 = local_response_normalization(pool1_3_3)
    conv2_3_3_reduce = conv_2d(pool1_3_3, 64, 1, activation='relu', name='conv2_3_3_reduce')
    conv2_3_3 = conv_2d(conv2_3_3_reduce, 192, 3, activation='relu', name='conv2_3_3')
    conv2_3_3 = local_response_normalization(conv2_3_3)
    pool2_3_3 = max_pool_2d(conv2_3_3, kernel_size=3, strides=2, name='pool2_3_3_s2')

    # 3a
    inception_3a_1_1 = conv_2d(pool2_3_3, 64, 1, activation='relu', name='inception_3a_1_1')
    inception_3a_3_3_reduce = conv_2d(pool2_3_3, 96, 1, activation='relu', name='inception_3a_3_3_reduce')
    inception_3a_3_3 = conv_2d(inception_3a_3_3_reduce, 128, filter_size=3, activation='relu', name='inception_3a_3_3')
    inception_3a_5_5_reduce = conv_2d(pool2_3_3, 16, filter_size=1, activation='relu', name='inception_3a_5_5_reduce')
    inception_3a_5_5 = conv_2d(inception_3a_5_5_reduce, 32, filter_size=5, activation='relu', name='inception_3a_5_5')
    inception_3a_pool = max_pool_2d(pool2_3_3, kernel_size=3, strides=1, name='inception_3a_pool')
    inception_3a_pool_1_1 = conv_2d(inception_3a_pool, 32, filter_size=1, activation='relu',
                                    name='inception_3a_pool_1_1')
    inception_3a_output = merge([inception_3a_1_1, inception_3a_3_3, inception_3a_5_5, inception_3a_pool_1_1],
                                mode='concat', axis=3)

    # 3b
    inception_3b_1_1 = conv_2d(inception_3a_output, 128, filter_size=1, activation='relu', name='inception_3b_1_1')
    inception_3b_3_3_reduce = conv_2d(inception_3a_output, 128, filter_size=1, activation='relu',
                                      name='inception_3b_3_3_reduce')
    inception_3b_3_3 = conv_2d(inception_3b_3_3_reduce, 192, filter_size=3, activation='relu', name='inception_3b_3_3')
    inception_3b_5_5_reduce = conv_2d(inception_3a_output, 32, filter_size=1, activation='relu',
                                      name='inception_3b_5_5_reduce')
    inception_3b_5_5 = conv_2d(inception_3b_5_5_reduce, 96, filter_size=5, name='inception_3b_5_5')
    inception_3b_pool = max_pool_2d(inception_3a_output, kernel_size=3, strides=1, name='inception_3b_pool')
    inception_3b_pool_1_1 = conv_2d(inception_3b_pool, 64, filter_size=1, activation='relu',
                                    name='inception_3b_pool_1_1')
    inception_3b_output = merge([inception_3b_1_1, inception_3b_3_3, inception_3b_5_5, inception_3b_pool_1_1],
                                mode='concat', axis=3, name='inception_3b_output')
    pool3_3_3 = max_pool_2d(inception_3b_output, kernel_size=3, strides=2, name='pool3_3_3')

    # 4a
    inception_4a_1_1 = conv_2d(pool3_3_3, 192, filter_size=1, activation='relu', name='inception_4a_1_1')
    inception_4a_3_3_reduce = conv_2d(pool3_3_3, 96, filter_size=1, activation='relu', name='inception_4a_3_3_reduce')
    inception_4a_3_3 = conv_2d(inception_4a_3_3_reduce, 208, filter_size=3, activation='relu', name='inception_4a_3_3')
    inception_4a_5_5_reduce = conv_2d(pool3_3_3, 16, filter_size=1, activation='relu', name='inception_4a_5_5_reduce')
    inception_4a_5_5 = conv_2d(inception_4a_5_5_reduce, 48, filter_size=5, activation='relu', name='inception_4a_5_5')
    inception_4a_pool = max_pool_2d(pool3_3_3, kernel_size=3, strides=1, name='inception_4a_pool')
    inception_4a_pool_1_1 = conv_2d(inception_4a_pool, 64, filter_size=1, activation='relu',
                                    name='inception_4a_pool_1_1')
    inception_4a_output = merge([inception_4a_1_1, inception_4a_3_3, inception_4a_5_5, inception_4a_pool_1_1],
                                mode='concat', axis=3, name='inception_4a_output')

    # 4b
    inception_4b_1_1 = conv_2d(inception_4a_output, 160, filter_size=1, activation='relu', name='inception_4a_1_1')
    inception_4b_3_3_reduce = conv_2d(inception_4a_output, 112, filter_size=1, activation='relu',
                                      name='inception_4b_3_3_reduce')
    inception_4b_3_3 = conv_2d(inception_4b_3_3_reduce, 224, filter_size=3, activation='relu', name='inception_4b_3_3')
    inception_4b_5_5_reduce = conv_2d(inception_4a_output, 24, filter_size=1, activation='relu',
                                      name='inception_4b_5_5_reduce')
    inception_4b_5_5 = conv_2d(inception_4b_5_5_reduce, 64, filter_size=5, activation='relu', name='inception_4b_5_5')
    inception_4b_pool = max_pool_2d(inception_4a_output, kernel_size=3, strides=1, name='inception_4b_pool')
    inception_4b_pool_1_1 = conv_2d(inception_4b_pool, 64, filter_size=1, activation='relu',
                                    name='inception_4b_pool_1_1')
    inception_4b_output = merge([inception_4b_1_1, inception_4b_3_3, inception_4b_5_5, inception_4b_pool_1_1],
                                mode='concat', axis=3, name='inception_4b_output')

    # 4c
    inception_4c_1_1 = conv_2d(inception_4b_output, 128, filter_size=1, activation='relu', name='inception_4c_1_1')
    inception_4c_3_3_reduce = conv_2d(inception_4b_output, 128, filter_size=1, activation='relu',
                                      name='inception_4c_3_3_reduce')
    inception_4c_3_3 = conv_2d(inception_4c_3_3_reduce, 256, filter_size=3, activation='relu', name='inception_4c_3_3')
    inception_4c_5_5_reduce = conv_2d(inception_4b_output, 24, filter_size=1, activation='relu',
                                      name='inception_4c_5_5_reduce')
    inception_4c_5_5 = conv_2d(inception_4c_5_5_reduce, 64, filter_size=5, activation='relu', name='inception_4c_5_5')
    inception_4c_pool = max_pool_2d(inception_4b_output, kernel_size=3, strides=1)
    inception_4c_pool_1_1 = conv_2d(inception_4c_pool, 64, filter_size=1, activation='relu',
                                    name='inception_4c_pool_1_1')
    inception_4c_output = merge([inception_4c_1_1, inception_4c_3_3, inception_4c_5_5, inception_4c_pool_1_1],
                                mode='concat', axis=3, name='inception_4c_output')

    # 4d
    inception_4d_1_1 = conv_2d(inception_4c_output, 112, filter_size=1, activation='relu', name='inception_4d_1_1')
    inception_4d_3_3_reduce = conv_2d(inception_4c_output, 144, filter_size=1, activation='relu',
                                      name='inception_4d_3_3_reduce')
    inception_4d_3_3 = conv_2d(inception_4d_3_3_reduce, 288, filter_size=3, activation='relu', name='inception_4d_3_3')
    inception_4d_5_5_reduce = conv_2d(inception_4c_output, 32, filter_size=1, activation='relu',
                                      name='inception_4d_5_5_reduce')
    inception_4d_5_5 = conv_2d(inception_4d_5_5_reduce, 64, filter_size=5, activation='relu', name='inception_4d_5_5')
    inception_4d_pool = max_pool_2d(inception_4c_output, kernel_size=3, strides=1, name='inception_4d_pool')
    inception_4d_pool_1_1 = conv_2d(inception_4d_pool, 64, filter_size=1, activation='relu',
                                    name='inception_4d_pool_1_1')
    inception_4d_output = merge([inception_4d_1_1, inception_4d_3_3, inception_4d_5_5, inception_4d_pool_1_1],
                                mode='concat', axis=3, name='inception_4d_output')

    # 4e
    inception_4e_1_1 = conv_2d(inception_4d_output, 256, filter_size=1, activation='relu', name='inception_4e_1_1')
    inception_4e_3_3_reduce = conv_2d(inception_4d_output, 160, filter_size=1, activation='relu',
                                      name='inception_4e_3_3_reduce')
    inception_4e_3_3 = conv_2d(inception_4e_3_3_reduce, 320, filter_size=3, activation='relu', name='inception_4e_3_3')
    inception_4e_5_5_reduce = conv_2d(inception_4d_output, 32, filter_size=1, activation='relu',
                                      name='inception_4e_5_5_reduce')
    inception_4e_5_5 = conv_2d(inception_4e_5_5_reduce, 128, filter_size=5, activation='relu', name='inception_4e_5_5')
    inception_4e_pool = max_pool_2d(inception_4d_output, kernel_size=3, strides=1, name='inception_4e_pool')
    inception_4e_pool_1_1 = conv_2d(inception_4e_pool, 128, filter_size=1, activation='relu',
                                    name='inception_4e_pool_1_1')
    inception_4e_output = merge([inception_4e_1_1, inception_4e_3_3, inception_4e_5_5, inception_4e_pool_1_1], axis=3,
                                mode='concat')
    pool4_3_3 = max_pool_2d(inception_4e_output, kernel_size=3, strides=2, name='pool_3_3')

    # 5a
    inception_5a_1_1 = conv_2d(pool4_3_3, 256, filter_size=1, activation='relu', name='inception_5a_1_1')
    inception_5a_3_3_reduce = conv_2d(pool4_3_3, 160, filter_size=1, activation='relu', name='inception_5a_3_3_reduce')
    inception_5a_3_3 = conv_2d(inception_5a_3_3_reduce, 320, filter_size=3, activation='relu', name='inception_5a_3_3')
    inception_5a_5_5_reduce = conv_2d(pool4_3_3, 32, filter_size=1, activation='relu', name='inception_5a_5_5_reduce')
    inception_5a_5_5 = conv_2d(inception_5a_5_5_reduce, 128, filter_size=5, activation='relu', name='inception_5a_5_5')
    inception_5a_pool = max_pool_2d(pool4_3_3, kernel_size=3, strides=1, name='inception_5a_pool')
    inception_5a_pool_1_1 = conv_2d(inception_5a_pool, 128, filter_size=1, activation='relu',
                                    name='inception_5a_pool_1_1')
    inception_5a_output = merge([inception_5a_1_1, inception_5a_3_3, inception_5a_5_5, inception_5a_pool_1_1], axis=3,
                                mode='concat')

    # 5b
    inception_5b_1_1 = conv_2d(inception_5a_output, 384, filter_size=1, activation='relu', name='inception_5b_1_1')
    inception_5b_3_3_reduce = conv_2d(inception_5a_output, 192, filter_size=1, activation='relu',
                                      name='inception_5b_3_3_reduce')
    inception_5b_3_3 = conv_2d(inception_5b_3_3_reduce, 384, filter_size=3, activation='relu', name='inception_5b_3_3')
    inception_5b_5_5_reduce = conv_2d(inception_5a_output, 48, filter_size=1, activation='relu',
                                      name='inception_5b_5_5_reduce')
    inception_5b_5_5 = conv_2d(inception_5b_5_5_reduce, 128, filter_size=5, activation='relu', name='inception_5b_5_5')
    inception_5b_pool = max_pool_2d(inception_5a_output, kernel_size=3, strides=1, name='inception_5b_pool')
    inception_5b_pool_1_1 = conv_2d(inception_5b_pool, 128, filter_size=1, activation='relu',
                                    name='inception_5b_pool_1_1')
    inception_5b_output = merge([inception_5b_1_1, inception_5b_3_3, inception_5b_5_5, inception_5b_pool_1_1], axis=3,
                                mode='concat')
    pool5_7_7 = avg_pool_2d(inception_5b_output, kernel_size=7, strides=1)
    pool5_7_7 = dropout(pool5_7_7, 0.4)

    # fc
    loss = fully_connected(pool5_7_7, output, activation='softmax')
    network = regression(loss, optimizer='momentum',
                         loss='categorical_crossentropy',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='googlenet_oxflowers17',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
    return model

'''