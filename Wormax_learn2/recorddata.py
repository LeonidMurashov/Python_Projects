from threading import Thread
import cv2
from pynput.mouse import Listener
from functools import partial
from grabscreen import grab_screen
import numpy as np
from getkeys import key_check
import os
import win32api
from image_preproc import preproc_img
from screen_consts import get_preproc_coordinates
import time

isPressed = False
def on_click(x, y, button, pressed):
	global isPressed
	isPressed = pressed
def detect_clicks():
	with Listener(on_click=partial(on_click)) as listener:
		listener.join()

BATCH_SIZE = 500
data = []
data_path = "data\\data_local\\"

def main():
	global data

	if not os.path.exists(data_path):
		os.mkdir(data_path)
		print("Created", os.path.dirname(os.path.abspath(data_path))+"\\" + data_path)

	frames = 0
	for file_name in os.listdir(data_path):
		num = int(file_name.split(sep="-")[2][:-4])
		if frames < num:
			frames = num
	print("Last save was", frames, "frames")

	thread = Thread(target=detect_clicks)
	thread.start()
	print("Start/Pause recording with Alt+T")
	paused = True

	while True:
		img = grab_screen()

		scr_W, scr_H = len(img[0]), len(img)
		img = preproc_img(img)

		keys = key_check()
		if "ALT" in keys and "T" in keys:
			paused ^= 1
			if paused:
				print("Stop recording, press Alt+T to continue")
			else:
				print("Start recording in 3 sec.")
				for i in list(range(3))[::-1]:
					time.sleep(1)
					print(i+1)
				print("recording!")
			time.sleep(1)

		if not paused:
			x, y = get_preproc_coordinates(win32api.GetCursorPos(), scr_W, scr_H)
			data.append([img, [x, y, isPressed, "Q" in keys, "W" in keys, "E" in keys]])

			if len(data) >= BATCH_SIZE:
				frames += len(data)
				print("Saved {}-{} frames".format(frames - BATCH_SIZE, frames))
				np.save(data_path + "frame-{}-{}.npy".format(frames - BATCH_SIZE, frames), data)
				data = []

if __name__=="__main__":
	main()


