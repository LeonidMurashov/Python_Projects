import cv2
from grabscreen import grab_screen
from screen_consts import GRAB_REGION, WIDTH, HEIGHT, roi
import numpy as np
import time

def bit_mask(img):
	ret, th1 = cv2.threshold(img, 70, 255, cv2.THRESH_TOZERO)
	th1 = cv2.cvtColor(th1,cv2.COLOR_BGR2GRAY)
	ret, th1 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY)
	return th1
'''
def max_intensivity(img):
	masked_data = img#cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
	for i in range(len(img)):
		for j in range(len(img[0])):
			masked_data[0] = 0
			masked_data[0] = 0
			masked_data[0] = 255

	#ret, th1 = cv2.threshold(img, 70, 255, cv2.THRESH_TOZERO)
	#th1 = cv2.cvtColor(th1,cv2.COLOR_BGR2GRAY)
	#ret, th1 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY)
	return masked_data'''

def detect_lose(img): # input RGB
	#print (np.average(np.array(img[:,:,0])), np.average(np.array(img[:,:,1])), np.average(np.array(img[:,:,2])))
	img = roi(img, [np.array([[WIDTH/2-12, HEIGHT/2-5], [WIDTH/2+12, HEIGHT/2-5], [WIDTH/2+12, HEIGHT/2+3], [WIDTH/2-12, HEIGHT/2+3]], np.int32)])
	b = np.average(np.array(img[:,:,2]))
	g = np.average(np.array(img[:,:,1]))
	r = np.average(np.array(img[:,:,0]))
	return r < 0.6 and g > 1.8 and b > 0.7#np.sum(np.array(img[:,:,1]))
	#return 17.0 < np.median(np.array(img)) < 19.0

	#img = cv2.medianBlur(img, 5)
	#th1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#kernel = np.ones((2,2),np.uint8)
	#th1 = cv2.dilate(th1,kernel, iterations=2)
	#th1 = cv2.erode(th1,kernel, iterations=4)

'''while 1:

	img = grab_screen(GRAB_REGION)
	img = (cv2.resize(img, (WIDTH, HEIGHT)))
	img = roi(img, [np.array([[WIDTH/2-12, HEIGHT/2-5], [WIDTH/2+12, HEIGHT/2-5], [WIDTH/2+12, HEIGHT/2+3], [WIDTH/2-12, HEIGHT/2+3]], np.int32)])
	img, lose = detect_lose(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
	print(lose)
	cv2.imshow('window', img)  # cv2.resize(bit_mask(img),(300,200)))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break'''

'''
while 1:
	img = grab_screen(GRAB_REGION)
	img = (cv2.resize(img, (WIDTH*3, HEIGHT*3)))
	res, img = cv2.threshold(img, 70, 255, cv2.THRESH_TOZERO)
	gray = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
	brit_img = np.array([[img[i][j][2] for j in range(len(img[0]))] for i in range(len(img))])


	#cv2.circle(img, (120, 120), 20, (100, 200, 80), -1)

	img = cv2.medianBlur(img, 3)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 2,
							   param1=5,
							   param2=10,
							   minRadius=0,
							   maxRadius=15)

	print ('\n\n----------',circles,'\n\n----------')
	#circles = np.uint16(np.around(circles))
	if circles != None:
		for i in circles[0, :]:
			cv2.circle(img, (i[0], i[1]), i[2], (255, 255, 255))'''
			#cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255),)
'''
	cv2.imshow('circles', brit_img)
	time.sleep(0.01)
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break


'''
'''def roi(img, vertices):
	# blank mask:
	mask = np.zeros_like(img)
	# filling pixels inside the polygon defined by "vertices" with the fill color
	cv2.fillPoly(mask, vertices, (255,255,255))
	# returning the image only where mask pixels are nonzero
	masked = cv2.bitwise_and(img, mask)
	return masked

while 1:
	img = grab_screen(GRAB_REGION)
	img = (cv2.resize(img, (WIDTH, HEIGHT)))
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	bitmasked = max_intensivity(img)

	cv2.imshow('window', bitmasked)#cv2.resize(bit_mask(img),(300,200)))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break'''