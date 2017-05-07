from screen_consts import WIDTH, HEIGHT, ROI_VERTICES, roi, GRAB_REGION, min_x, min_y, max_y, max_x, cx, cy, kx, ky
import cv2
from grabscreen import grab_screen
import win32api, win32con
from getkeys import key_check
import time
from CV_helpfile import detect_lose, recognize_score

def mouse_down(c):
	win32api.SetCursorPos((c[0], c[1]))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, c[0], c[1], 0, 0)

def mouse_up(c):
	win32api.SetCursorPos((c[0], c[1]))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, c[0], c[1], 0, 0)

def mouse(c, press):
	if press:
		mouse_down(c)
	else:
		mouse_up(c)

def coordinates_wrapper(mx, my):
	mx = int(mx * kx + cx)
	my = int(my * ky + cy)
	if mx > max_x:  mx = max_x
	if mx < min_x:  mx = min_x
	if my > max_y:  my = max_y
	if my < min_y:  my = min_y
	return (mx, my)

def ulp(): mouse(coordinates_wrapper(-0.5, -0.5), True)
def up(): mouse(coordinates_wrapper(0, -0.5), True)
def urp(): mouse(coordinates_wrapper(0.5, -0.5), True)
def lp(): mouse(coordinates_wrapper(-0.5, 0), True)
def rp(): mouse(coordinates_wrapper(0.5, 0), True)
def dlp(): mouse(coordinates_wrapper(-0.5, 0.5), True)
def dp(): mouse(coordinates_wrapper(0, 0.5), True)
def drp(): mouse(coordinates_wrapper(0.5, 0.5), True)
def ul(): mouse(coordinates_wrapper(-0.5, -0.5), False)
def u(): mouse(coordinates_wrapper(0, -0.5), False)
def ur(): mouse(coordinates_wrapper(0.5, -0.5), False)
def l(): mouse(coordinates_wrapper(-0.5, 0), False)
def r(): mouse(coordinates_wrapper(0.5, 0), False)
def dl(): mouse(coordinates_wrapper(-0.5, 0.5), False)
def d(): mouse(coordinates_wrapper(0, 0.5), False)
def dr(): mouse(coordinates_wrapper(0.5, 0.5), False)


class Environment:
	actions = [ul, u, ur, l, r, dl, d, dr]#, ulp, up, urp, lp, rp, dlp, dp, drp]
	last_score = 10
	was_huge = 0
	def __init__(self):
		pass

	def reset(self):
		pass

	def step(self, action):

		keys = key_check()
		if 'T' in keys:
			print("Paused!")
			time.sleep(2)
			while 'T' not in key_check():
				time.sleep(0.01)
			print("Unpaused!")
			time.sleep(1)

		img = grab_screen(region=GRAB_REGION)
		score = recognize_score(img)
		delta = 0
		if score != -1 and score != 0:
			delta = (score - self.last_score)
			if abs(delta) > 100 and self.was_huge < 3:
				self.was_huge += 1
				delta = 0
			else:
				self.was_huge = 0
				self.last_score = score
		'''if abs(delta) > 20 and self.was_huge < 4 or score == 0:
			delta = 0
			self.was_huge += 1

		else:
			self.was_huge = 0'''

		self.actions[action]()
		img = roi(cv2.resize(img, (WIDTH, HEIGHT)), ROI_VERTICES)
		lose = detect_lose(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

		if lose:
			mouse_up(coordinates_wrapper(0,0))
			mouse_down(coordinates_wrapper(0,0))
			mouse_up(coordinates_wrapper(0,0))
			self.last_score = 10
		if delta:
			print(delta)
		return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), delta, lose, False # s_t1, r_t, terminal, info =
		#time.sleep(0.01)

	def reset(self):
		img = grab_screen(region=GRAB_REGION)
		img = roi(cv2.resize(img, (WIDTH, HEIGHT)), ROI_VERTICES)
		return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)




'''def main():
	time.sleep(1)
	paused = False
	while 1:
		img = grab_screen(region=GRAB_REGION)
		img = cv2.cvtColor(roi(cv2.resize(img, (WIDTH, HEIGHT)), ROI_VERTICES), cv2.COLOR_BGR2RGB)

		if not paused:
			for i in actions:
				i()
				time.sleep(0.01)
			lose = detect_lose(img)
			print(lose)
			if lose:
				mouse_up(coordinates_wrapper(0,0))
				mouse_down(coordinates_wrapper(0,0))
				mouse_up(coordinates_wrapper(0,0))

		keys = key_check()
		if 'T' in keys:
			if paused:
				paused = False
				time.sleep(1)
			else:
				paused = True
				time.sleep(2)
main()'''