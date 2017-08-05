from neural_network import build_model
from autoencoder_preproc import build_autoencoder, load_autoencoder, save_autoencoder
import tensorflow as tf

m1 = build_model(1, 3)
build_autoencoder()

m1.save("m1")
save_autoencoder()

tf.reset_default_graph()

m1 = build_model(1,3)
m2 = build_autoencoder()
m1.load("m1")
load_autoencoder()

