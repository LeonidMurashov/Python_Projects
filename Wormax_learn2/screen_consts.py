from math import atan2, sin, cos, pi

# my screen 1680*1050
# Yura screen 1280*1024
# mom screen 1366*768
target_resolution = (1280, 719)#1050*(1280/1680))

WIDTH = 160
HEIGHT = 100


def get_preproc_coordinates(c, scr_W, scr_H):
	x = c[0]
	y = c[1]

	a = max(scr_H, scr_W)
	return round((x - scr_W/2)/(a/2), 2), round((y - scr_H/2)/(a/2), 2)


def decode_coordinates(x, y, scr_W, scr_H):
	x = int(x*scr_W/2 + scr_W/2)
	y = int(y*scr_H/2 + scr_H/2)
	return x,y


def get_angle(x, y):
	return atan2(y, x)

def get_direction(x, y, n_classes = 12):
	return round(get_angle(x, y)/2/pi*n_classes)%n_classes#round((get_angle(x, y)+pi)/(2*pi)*nclasses+6)%nclasses

def get_cartesian(fi, scr_W, scr_H):
	a = min(scr_W, scr_H)/2
	return int(a*cos(fi)/2 + scr_W/2), int(a*sin(fi)/2 + scr_H/2)

def get_coordinates_from_direction(dir, scr_W, scr_H, n_classes = 12):
	angle = (dir / n_classes) * 2 * pi
	return get_cartesian(angle, scr_W, scr_H)


#####9####
###8###10##
##7#####11#
#6#######0#
##5#####1##
###4###2###
#####3####


'''import win32api, win32con
import time

def mouse_up(x, y):
	win32api.SetCursorPos((x, y))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

n_classes = 12
time.sleep(2)
while True:
	for i in range(n_classes):
		x, y = get_preproc_coordinates(win32api.GetCursorPos(), 1650, 1050)
		dir = i
		#x, y = get_coordinates_from_direction(dir, 1650, 1050)
		#mouse_up(x,y)
		a, b = x,y#get_preproc_coordinates((x, y), 1650, 1050)
		dir_get = get_direction(a, b, n_classes)
		print(dir,dir_get,"  ", x, y)
		print()
		#
		time.sleep(0.1)'''