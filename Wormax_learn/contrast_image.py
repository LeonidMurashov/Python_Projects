import cv2
from grabscreen import grab_screen
from screen_consts import GRAB_REGION

def contrast_image(img):
	gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	mask = ret,thresh1 = cv2.threshold(img,(127,0,0),(255,255,255),cv2.THRESH_BINARY)

	return gray_img

while 1:
	img = contrast_image(grab_screen(GRAB_REGION))
	cv2.imshow('window', cv2.resize(img,(200,120)))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break