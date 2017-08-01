import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tensorflow as tf

MODEL_NAME = "Simple-{}".format(0)

def build_model(input, output, lr, sess):
    network = input_data(shape=[None, input], name='input')
    network = fully_connected(network, 10, activation='sigmoid')
    network = fully_connected(network, 10, activation='sigmoid')
    network = fully_connected(network, output, activation='sigmoid')
    network = regression(network, optimizer='momentum',
                         loss='mean_square',
                         learning_rate=lr, name='targets')

    model = tflearn.DNN(network, checkpoint_path='model',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log', session=sess )
    return model

X = np.array([[0,0],[0,1],[1,0],[1,1]]).reshape(-1, 2)
y = np.array([1,0,0,1]).reshape(-1, 1)

with tf.Session() as sess:
    with tf.device('/cpu:0'):

        print(X)
        model = build_model(2,1,0.01, sess)
        model.fit({'input': X}, {'targets': y}, n_epoch=1,
                  snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

        X_test = np.array([ [i,j] for j in np.arange(0,1,0.1) for i in np.arange(0,1,0.1)]).reshape(-1, 2)

        fig = plt.figure()
        ax = fig.add_subplot(111,projection='3d')
        ax.scatter(X_test[:,0],X_test[:,1],clf.predict(X_test))
        plt.show()




'''import pygame
from pygame import *

# Py game consts
DISPLAY = (1000, 700)  # Группируем ширину и высоту в одну переменную

pygame.init()
screen = pygame.display.set_mode(DISPLAY)
# PyGame init
pygame.display.set_caption("Super Mario Boy")
bg = Surface(DISPLAY)
BACKGROUND_COLOR = "#555555"
bg.fill(Color(BACKGROUND_COLOR))

while True:
	for e in pygame.event.get(): # Обрабатываем события
		if e.type == QUIT:
				raise (SystemExit, "QUIT")
	screen.blit(bg, (0,0))
	pygame.display.update()'''