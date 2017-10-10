import time
import win32api
import win32con

import cv2
import numpy as np
import tensorflow as tf

from getkeys import key_check
from grabscreen import grab_screen
from image_preproc import preproc_img
from neural_network import build_model
from screen_consts import decode_coordinates
from trash.autoencoder_preproc import autoencode, load_autoencoder, build_autoencoder


def mouse_down(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

def mouse_up(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

LR = 1e-3
MODEL_NAME = 'models/wrm13-encoded-1e-04-15-ep-407k-data.model'

tf.reset_default_graph()

model2 = build_model(LR, 4)
model2.load(MODEL_NAME)
build_autoencoder()
load_autoencoder()

print("Start/Pause action with Alt+T")
paused = True

while True:
	img = grab_screen()

	scr_W, scr_H = len(img[0]), len(img)
	img = preproc_img(img)

	keys = key_check()
	if "ALT" in keys and "T" in keys:
		paused ^= 1
		if paused:
			print("Stop action, press Alt+T to continue")
		else:
			print("Start action in 3 sec.")
			for i in list(range(3))[::-1]:
				time.sleep(1)
				print(i + 1)
			print("action!")
		time.sleep(1)
	if "C" in keys:
		offset = -75
		mouse_up(scr_W//2, scr_H//2+offset)
		mouse_down(scr_W//2, scr_H//2+offset)
		mouse_up(scr_W//2, scr_H//2+offset)

	if not paused:
		prep_img = autoencode(img).reshape(2080)
		prediction = np.argmax(model2.predict(prep_img)[0])
		x, y = decode_coordinates(prediction[0], prediction[1], scr_W, scr_H)
		if prediction[2] > 0:
			mouse_up(x, y)
		else:
			mouse_down(x, y)
		print(np.round(model2.predict(prep_img), 2), prediction)

		if cv2.waitKey(25) & 0xFF == ord('p'):
			cv2.destroyAllWindows()
			break