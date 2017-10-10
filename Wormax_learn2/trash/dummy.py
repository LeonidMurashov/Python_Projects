import tensorflow as tf

from neural_network import build_model
from trash.autoencoder_preproc import build_autoencoder, load_autoencoder, save_autoencoder

m1 = build_model(1, 3)
m1.save("m1")
build_autoencoder()

save_autoencoder()

tf.reset_default_graph()

m1 = build_model(1,3)
m2 = build_autoencoder()
m1.load("m1")
load_autoencoder()

