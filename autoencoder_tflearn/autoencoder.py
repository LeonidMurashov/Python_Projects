import tflearn
import numpy as np
from tflearn.layers.conv import conv_2d, max_pool_2d, upsample_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.recurrent import gru


input_img = input_data(shape=(28, 28, 1), name='input')                 ; print(input_img.shape)
x = conv_2d(input_img, 16, (3, 3), activation='relu', padding='same')   ; print(x.shape)
x = max_pool_2d(x, (2, 2), padding='same')                              ; print(x.shape)
x = conv_2d(x, 8, (3, 3), activation='relu', padding='same')            ; print(x.shape)
x = max_pool_2d(x, (2, 2), padding='same')                              ; print(x.shape)
x = conv_2d(x, 8, (3, 3), activation='relu', padding='same')            ; print(x.shape)
print("here")
encoded = max_pool_2d(x, (2, 2), padding='same')                        ; print(x.shape)# at this point the representation is (4, 4, 8) i.e. 128-dimensional
x = conv_2d(encoded, 8, (3, 3), activation='relu', padding='same')      ; print(x.shape)
print("here")
x = upsample_2d (x, (2, 2))                                             ; print(x.shape)
x = conv_2d(x, 8, (3, 3), activation='relu', padding='same')            ; print(x.shape)
x = upsample_2d (x, (2, 2))                                             ; print(x.shape)
x = conv_2d(x, 16, (3, 3), activation='relu')                           ; print(x.shape)
x = upsample_2d (x, (2, 2))                                             ; print(x.shape)
decoded = conv_2d(x, 1, (3, 3), activation='sigmoid', padding='same')   ; print(x.shape)

autoencoder = regression(decoded, optimizer='momentum',loss='categorical_crossentropy',
                         learning_rate=0.001, name='targets')
model = tflearn.DNN(autoencoder, checkpoint_path='autoencoder',
                        max_checkpoints=1, tensorboard_verbose=0, tensorboard_dir='log')


from keras.datasets import mnist
import numpy as np

(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1))  # adapt this if using `channels_first` image data format
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1))  # adapt this if using `channels_first` image data format

model.fit({'input': x_train}, {'targets': x_train}, n_epoch=1, validation_set=({'input': x_test}, {'targets': x_test}),
				snapshot_step=500, show_metric=True, run_id="model_alexnet", shuffle=True,)
