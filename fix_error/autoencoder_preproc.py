import tflearn
import numpy as np
from tflearn.layers.conv import conv_2d, max_pool_2d, upsample_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.recurrent import gru
import cv2
import tensorflow as tf

WIDTH, HEIGHT = 160, 100
CHANNELS = 3
MODEL_NUMBER = 2
MODEL_NAME = 'autoencoder-'+str(MODEL_NUMBER)

autoencoder, INPUT, HIDDEN_STATE, OUTPUT = None,None,None,None

def build():
	input_img = input_data(shape=(HEIGHT, WIDTH, CHANNELS), name='input');print(input_img.shape)
	INPUT = input_img
	x = conv_2d(input_img, 16, (3, 3), activation='relu', padding='same');print(x.shape)
	x = max_pool_2d(x, (2, 2), padding='same');print(x.shape)
	x = conv_2d(x, 8, (3, 3), activation='relu', padding='same');print(x.shape)
	x = max_pool_2d(x, (2, 2), padding='same');print(x.shape)
	x = conv_2d(x, 8, (3, 3), activation='relu', padding='same');print(x.shape)
	encoded = max_pool_2d(x, (2, 2), padding='same');print(encoded.shape)  # at this point the representation is (4, 4, 8) i.e. 128-dimensional

	HIDDEN_STATE = encoded
	print("middle")

	x = conv_2d(encoded, 8, (3, 3), activation='relu', padding='same', name='input2');print(x.shape)
	x = upsample_2d(x, (2, 2));print(x.shape)
	x = conv_2d(x, 8, (3, 3), activation='relu', padding='same');print(x.shape)
	x = upsample_2d(x, (2, 2));print(x.shape)
	x = conv_2d(x, 16, (3, 3), activation='relu', padding='same');print(x.shape)
	x = upsample_2d(x, (2, 2));print(x.shape)
	decoded = conv_2d(x, CHANNELS, (3, 3), activation='sigmoid', padding='same');print(decoded.shape)
	OUTPUT = decoded
	autoencoder = regression(decoded, optimizer='momentum', loss='mean_square',
							 learning_rate=0.005, name='targets')
	model = tflearn.DNN(autoencoder, checkpoint_path=MODEL_NAME,
						max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')
	return model, INPUT, HIDDEN_STATE, OUTPUT

def encode (X):
    if len (X.shape) < 2:
        X = X.reshape (1, -1)

    tflearn.is_training (False, autoencoder.session)
    res = autoencoder.session.run (HIDDEN_STATE, feed_dict={INPUT.name:X})
    return res

def decode (X):
    if len (X.shape) < 2:
        X = X.reshape (1, -1)

    #just to pass something to place_holder
    zeros = np.zeros ((1,HEIGHT,WIDTH,CHANNELS))

    tflearn.is_training (False, autoencoder.session)
    res = autoencoder.session.run (OUTPUT, feed_dict={INPUT.name:zeros, HIDDEN_STATE.name:X})
    return res

def load_autoencoder():
	global autoencoder
	autoencoder = autoencoder.load("m2")

def build_autoencoder():
	global autoencoder
	autoencoder, INPUT, HIDDEN_STATE, OUTPUT = build()

def save_autoencoder():
	autoencoder.save("m2")

def autoencode(img):
	img = img / 255.
	img = img.reshape(-1,HEIGHT, WIDTH, CHANNELS)
	#a = (model.predict(img))
	a = encode(img).reshape(52,40)
	return a#[0]

def autodecode(img):
	img = img / 255.
	img = img.reshape(-1,HEIGHT, WIDTH, CHANNELS)
	a = (autoencoder.predict(img))
	return a[0]