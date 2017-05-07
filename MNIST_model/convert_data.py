import os
import numpy as np
from PIL import Image
import random
pics = []
targets = []
digits_path = 'D:/Python/MNIST_model/digits/'

for i in os.listdir(digits_path):
	for j in os.listdir(digits_path + i + '/'):
		img = Image.open(digits_path + i + '/' + j)
		pics.append(np.array(img, dtype=int).flatten())
		if i == 'conf':
			targets.append(-1)
		elif i == 'none':
			targets.append(0)
		else:
			targets.append(int(i))
seed = random.randint(0,10000)
np.random.seed(seed)
np.random.shuffle(pics)
np.random.seed(seed)
np.random.shuffle(targets)
np.save('my_MNIST_pics.npy', pics)
np.save('my_MNIST_tgts.npy', targets)



'''pic = Image.open('D:/Python/MNIST_model/digits/' + i)
	pic = pic.convert('1')
	pics.append(np.array(pic, dtype=int).flatten())
	targets.append(int(i[3]) if i[3] != '-' else -1)'''