import os

import numpy as np

from trash.autoencoder_preproc import autoencode

folder_in = "preprocessed_data_local_notshuffled/"
folder_out = "preprocessed_encoded_notshuffled/"
listdir = os.listdir(folder_in)
for i, file in enumerate(listdir):
	data = np.load(folder_in + file)
	encoded_data = []

	for row in data:
		encoded_data.append([ autoencode(row[0]).reshape(2080), [row[1][0], row[1][1], 1 if row[1][2] else -1]])
	np.save(folder_out + file, encoded_data)
	print(i/len(listdir), "Done.")

print("All done.")