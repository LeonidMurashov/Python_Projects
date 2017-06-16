import numpy as np
import os
from image_preproc import prepare_image
from screen_consts import get_direction
import random
from CV_helpfile import detect_any_worms, rotated_frames, get_one_hot
data = []
data_path = "data\\"
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

print("Loaded {} frames".format(len(data)))
print("Start preprocessing")

classes = np.zeros([n_classes])
dels_array = []
no_worms = 0;len_data = len(data)

for i in range(len(data)):
	# Creating X
	img = data[i][0]
	if np.average(img) < 100:
		data[i][0], food_map = prepare_image(img, True)
		if not detect_any_worms(img, food_map):
			dels_array.append(i)
			no_worms += 1
			continue

		one_hot = get_one_hot(data[i][1][0], data[i][1][1], n_classes)
		#data[i][1] = one_hot
		classes[np.argmax(one_hot)] += 1

	else:
		dels_array.append(i)

	if i in range(0, len(data), len(data)//10):
		print(str(round(i/len(data)*100)) + "% complete")

data = np.delete(data,dels_array, 0)

print("No worms:", no_worms)
print("deleted:", len_data-len(data))

np.random.shuffle(data)
print("Unbalanced data:", np.round(classes))
balance_to = np.min(classes)
print("Start balancing to", balance_to)
dels_array.clear()
for i, row in enumerate(data):
	row_class = get_direction(row[1][0], row[1][1], n_classes)
	if classes[row_class]-balance_to >= 1:
		dels_array.append(i)
		classes[row_class] -= 1

data = np.delete(data, dels_array, 0)
print("Balanced len:", len(data))
print("Overall deleted:", len_data - len(data))

print("\nMultiplying dataset(x4)")
multiplied_data = []
saved = 0
classes = np.zeros_like(classes)
for i,frame in enumerate(data):
	###isPressed = (data[i][1][2] or data[i][1][3])*2 - 1
	rotated = rotated_frames(frame[0], frame[1][0], frame[1][1], n_classes)

	for j in rotated:
		classes += j[1]
		hot = np.argmax(j[1])
		j[1][hot - 1] = 0.1
		j[1][hot] = 0.8
		j[1][(hot + 1) % n_classes] = 0.1

	multiplied_data += rotated

	if len(multiplied_data) >= BATCH_SIZE:
		np.save("preprocessed_data\\" + "preprocessed-{}-{}.npy".format(saved, saved+BATCH_SIZE), multiplied_data[0:BATCH_SIZE])
		saved += BATCH_SIZE
		del multiplied_data[0:BATCH_SIZE]

	if i in range(0, len(data), len(data)//10):
		print(str(round(i/len(data)*100)) + "% complete")
del data

if len(multiplied_data) > 0:
	np.save("preprocessed_data\\" + "preprocessed-{}-{}.npy".format(saved, saved+len(multiplied_data)), multiplied_data[0:len(multiplied_data)])
	saved += len(multiplied_data)


'''classes = np.zeros([n_classes])
for i in multiplied_data:
	classes += i[1]
	hot = np.argmax(i[1])
	i[1][hot - 1] = 0.1
	i[1][hot] = 0.8
	i[1][(hot + 1) % n_classes] = 0.1'''
print("Final classes:", classes)
print("Final len:", len(multiplied_data))

'''# Save by batches
print("Start saving")
for i in range(0, len(multiplied_data), BATCH_SIZE):
	print(str(round(i/len(multiplied_data)*100)) + "% complete")
	j = min(i + BATCH_SIZE, len(multiplied_data)-1)
	np.save("preprocessed_data\\" + "preprocessed-{}-{}.npy".format(i, j), multiplied_data[i:j])'''
print("Done.")
exit()