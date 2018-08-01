from getkeys import key_check
import win32api, win32con
import time

def mouse_down(x,y):
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)

def mouse_up(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

print("Start/Pause action with Alt+T")
paused = True

while True:
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

	if not paused:

		mouse_up(650, 500)
		