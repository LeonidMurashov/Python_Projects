from alexnet_easy import modified_alexnet
from screen_consts import WIDTH, HEIGHT, get_coordinates_from_direction
from grabscreen import grab_screen
from image_preproc import preproc_img
from getkeys import key_check
from image_preproc import prepare_image
import win32api, win32con
import time
import numpy as np
import cv2

def mouse_down(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

def mouse_up(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

LR = 1e-3
EPOCHS = 20
MODEL_NAME = 'models/wrm14-easy-0.001-15-ep-0.5M-data.model'
n_classes = 12

model = modified_alexnet(WIDTH, HEIGHT, 2, LR, n_classes)
model.load(MODEL_NAME)

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
		prep_img = prepare_image(img).reshape(-1, WIDTH, HEIGHT,2)
		prediction = np.argmax(model.predict(prep_img)[0])
		x, y = get_coordinates_from_direction(prediction, scr_W, scr_H, n_classes)
		mouse_up(x, y)
		print(np.round(model.predict(prep_img), 2), prediction)

		if cv2.waitKey(25) & 0xFF == ord('p'):
			cv2.destroyAllWindows()
			break