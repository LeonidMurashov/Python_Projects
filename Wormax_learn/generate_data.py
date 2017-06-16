import os
import time
import win32api
from functools import partial
from threading import Thread
import cv2
import numpy as np
from getkeys import key_check
from grabscreen import grab_screen
from pynput.mouse import Listener
from screen_consts import WIDTH, HEIGHT, roi


isPressed = False
samples_count = 0

folder = 'learn_data_colored/'
samples_in_file = 1000
training_data = []

def on_click(x, y, button, pressed):
	global isPressed
	isPressed = pressed
def detect_clicks():
	with Listener(on_click=partial(on_click)) as listener:
		listener.join()

for fname in os.listdir(folder):
	arr = np.load(folder+fname)
	if len(arr) < samples_in_file:
		training_data = arr
	else:
		samples_count += len(arr)
print("Samples found ", samples_count)
#print(np.shape(training_data))
def main():
	global training_data, samples_count

	for i in list(range(4))[::-1]:
		print(i+1)
		time.sleep(1)

	thread = Thread(target=detect_clicks)
	vertices = np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT],[WIDTH-85, HEIGHT],[WIDTH-85, HEIGHT-15],[WIDTH-105, HEIGHT-15],[WIDTH-105, HEIGHT], [0, HEIGHT],
						 ], np.int32)

	paused = True
	print("Press T to start (and pause/unpause)")
	while True:
		img = cv2.cvtColor(cv2.resize(grab_screen(region=(0, 125, 1000, 725)),(WIDTH,HEIGHT)), cv2.COLOR_BGR2RGB)
		img = roi(img,[vertices])
		#cv2.imshow("SCREEN", screen)
	   # time.sleep(0.1)

		if not paused:
			x, y = win32api.GetCursorPos()
			training_data.append([img, [x, y, isPressed]])
			if len(training_data) >= samples_in_file:
				samples_count += len(training_data)
				print(samples_count)
				np.save(folder + "training_data-{}-{}".format(samples_count - samples_in_file, samples_count), training_data)
				training_data = []

		keys = key_check()
		if 'T' in keys:
			if paused:
				paused = False
				print('unpaused!')
				time.sleep(1)
			else:
				print('Pausing!')
				paused = True
				time.sleep(1)

		cv2.imshow('window', img)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break

main()

'''if os.path.isfile(file_name):
	print('File exists, loading previous data!')
	training_data = list(np.load(file_name))
else:
	print('File does not exist, starting fresh!')
	training_data = []'''