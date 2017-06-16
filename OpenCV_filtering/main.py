import cv2
import numpy as np


# 'optional' argument is required for trackbar creation parameters
def nothing():
	pass

# Capture video from the stream
cv2.namedWindow('Colorbars')

# assign strings for ease of coding
hh = 'Hue High'
hl = 'Hue Low'
sh = 'Saturation High'
sl = 'Saturation Low'
vh = 'Value High'
vl = 'Value Low'
wnd = 'Colorbars'
# Begin Creating trackbars for each
cv2.createTrackbar(hl, wnd, 0, 179, nothing)
cv2.createTrackbar(hh, wnd, 0, 179, nothing)
cv2.createTrackbar(sl, wnd,0,255,nothing)
cv2.createTrackbar(sh, wnd, 0, 255, nothing)
cv2.createTrackbar(vl, wnd, 0, 255, nothing)
cv2.createTrackbar(vh, wnd,0,255,nothing)

HSVLOW = np.array([0, 0, 240])
HSVHIGH = np.array([179, 106, 255])

cv2.setTrackbarPos(hl, wnd, HSVLOW[0])
cv2.setTrackbarPos(hh, wnd, HSVHIGH[0])
cv2.setTrackbarPos(sl, wnd, HSVLOW[1])
cv2.setTrackbarPos(sh, wnd, HSVHIGH[1])
cv2.setTrackbarPos(vl, wnd, HSVLOW[2])
cv2.setTrackbarPos(vh, wnd, HSVHIGH[2])

cv2.setWindowProperty(wnd,cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_NORMAL)

# begin our 'infinite' while loop
while (1):
	# read the streamed frames (we previously named this cap)
	frame = cv2.resize(cv2.imread("D:\\Python\\Wormax_learn2\\test_it.jpg"), (640,400), interpolation=cv2.INTERSECT_NONE)

	# it is common to apply a blur to the frame
	#frame = cv2.GaussianBlur(frame, (5, 5), 0)

	# convert from a BGR stream to an HSV stream
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# read trackbar positions for each trackbar
	hul = cv2.getTrackbarPos(hl, wnd)
	huh = cv2.getTrackbarPos(hh, wnd)
	sal = cv2.getTrackbarPos(sl, wnd)
	sah = cv2.getTrackbarPos(sh, wnd)
	val = cv2.getTrackbarPos(vl, wnd)
	vah = cv2.getTrackbarPos(vh, wnd)
	# make array for final values
	HSVLOW = np.array([hul, sal, val])
	HSVHIGH = np.array([huh, sah, vah])
	mask = cv2.inRange(hsv, HSVLOW, HSVHIGH)
	res = cv2.bitwise_and(frame, frame, mask=mask)
	_,res = cv2.threshold(res,0, 255, cv2.THRESH_BINARY)

	cv2.imshow(wnd, res)
	cv2.imshow("fefe", frame)

	k = cv2.waitKey(25) & 0xFF
	if k == ord('p'):
		break

cv2.destroyAllWindows()