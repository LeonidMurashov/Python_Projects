from joblib import Parallel, delayed
import time
import multiprocessing
from image_preproc import *
from CV_helpfile import *

def processInput(img):
	a, food_map = prepare_image(img, True)
	b = detect_any_worms(img, food_map)
	return a,b

if __name__ == "__main__":
	###################################
	data = []
	data_path = "data\\delme\\"
	BATCH_SIZE = 10000
	n_classes = 12

	listdir = []
	for dir in os.listdir(data_path):
		listdir += map(lambda x: dir + "\\" + x,os.listdir(data_path + dir))
	random.shuffle(listdir)

	print("Start reading data")

	for file_name in listdir:
		if len(data) == 0:
			data = np.load(data_path + file_name)
		else:
			data = np.concatenate((data, np.load(data_path + file_name)))

	print("Start preprocessing")
	############################################

	inputs = data[:,0]
	t = time.clock()
	num_cores = multiprocessing.cpu_count()
	results = Parallel(n_jobs=num_cores)(delayed(processInput)(i) for i in inputs)
	print("Parallel took:", time.clock() - t)

	results = []
	t = time.clock()
	for i in inputs:
		results.append(processInput(i))
	print("Loop took:", time.clock() - t)
