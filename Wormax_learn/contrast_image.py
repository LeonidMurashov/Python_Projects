import cv2
import random
import numpy as np

while 1:
	arr = np.load("learn_data_balanced_bool/training_data_balanced-0.npy")
	for i in range(random.randint(0, len(arr) - 1000), len(arr)):
		cv2.imshow("name", arr[i][0])
		print(arr[i][1])
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
