import cv2
import pytesseract

from grabscreen import grab_screen
from screen_consts import GRAB_REGION, WIDTH, HEIGHT, roi, ACTUAL_HEIGHT, ACTUAL_WIDTH
import numpy as np
import time
from PIL import Image
import _pickle as cPickle
import random
from pytesseract import image_to_string
from sklearn.ensemble import RandomForestClassifier
import copy
from getkeys import key_check

def bit_mask(img):
	ret, th1 = cv2.threshold(img, 70, 255, cv2.THRESH_TOZERO)
	th1 = cv2.cvtColor(th1,cv2.COLOR_BGR2GRAY)
	ret, th1 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY)
	return th1

def detect_lose(img): # input RGB
	img = roi(img, [np.array([[WIDTH/2-12, HEIGHT/2-5], [WIDTH/2+12, HEIGHT/2-5], [WIDTH/2+12, HEIGHT/2+3], [WIDTH/2-12, HEIGHT/2+3]], np.int32)])
	b = np.average(np.array(img[:,:,2]))
	g = np.average(np.array(img[:,:,1]))
	r = np.average(np.array(img[:,:,0]))
	return r < 0.6 and g > 1.5 and b > 0.5
	#print (np.average(np.array(img[:,:,0])), np.average(np.array(img[:,:,1])), np.average(np.array(img[:,:,2])))
	#cv2.imshow('window', img)

def recognize_score(img):
	img = img[int(ACTUAL_HEIGHT/2-75):int(ACTUAL_HEIGHT/2-55), int(ACTUAL_WIDTH-50):int(ACTUAL_WIDTH-10)]

	for i in range(len(img)):
		for j in range(len(img[0])):
			if img[i][j][0] > 252 and img[i][j][1] > 252 and img[i][j][2] > 252:
				img[i][j] = 255
			else:
				img[i][j] = 0
	img = cv2.dilate(img, np.ones((2,2),np.uint8))
	chars = [img[:,0:10], img[:,10:20], img[:,20:30], img[:,30:40]] #10x20
	for i in range(4):
		chars[i] = Image.fromarray(chars[i])
		chars[i] = chars[i].convert('1')
		chars[i] = np.array(chars[i], dtype=int).flatten()

	score = 0
	with open('digits_classifier.pkl', 'rb') as fid:
		model = cPickle.load(fid)
		pred = model.predict(chars)
		if -1 in pred:
			return -1#, img
		pred = pred[::-1]
		for i in range(4):
			if pred[i] != -1:
				score += pred[i] * 10**i

	return score#, img


'''if saving:
	chars[i].save('digits/dig-{}.png'.format(random.randint(0,10000)))
	#char = copy.deepcopy(np.reshape(np.array(list(chars[i].getdata()))*255,(20,10)))
	print('Saving')'''
'''while 1:
	img = grab_screen(GRAB_REGION)
	score,ch = recognize_score(img)
	print(score)
	cv2.imshow("name",ch)
	# cv2.resize(bit_mask(img),(300,200)))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break'''
#result.save('digits/dig-{}.png'.format(random.randint(0,1000)))

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