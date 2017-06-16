import os
import numpy as np

# my screen 1680*1050
# Yura screen 1280*1024
# mom screen 1366*768
'''data_path = "data\\data_local\\"
for file in os.listdir(data_path):
	data = np.load(data_path + file)
	for row in data:
		row[1][1] = round(row[1][1]*(1050/1680), 2)
	np.save(data_path + file, data)
print("Saved local")

data_path = "data\\data_yura\\"
for file in os.listdir(data_path):
	data = np.load(data_path + file)
	for row in data:
		row[1][1] = round(row[1][1]*(1024/1280), 2)
	np.save(data_path + file, data)
print("Saved yura")


data_path = "data\\data_local\\"
for file in os.listdir(data_path):
	data = np.load(data_path + file)
	for row in data:
		row[1][1] = round(row[1][1]*(768/1366), 2)
	np.save(data_path + file, data)
print("Saved mom")

print("Done.")'''