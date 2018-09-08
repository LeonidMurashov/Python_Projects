# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np

def make_null_image(img):
    img_exp = np.zeros((28,28))
    img_preproc = 255 - cv2.resize(img, (12, 16), interpolation=cv2.INTERSECT_NONE)
    img_exp[6:-6,8:-8] = img_preproc
    return img_exp

def recognize_digit(img):
    # Resize the image
    img_exp = np.zeros((28,28))
    img_preproc = 255 - cv2.resize(img, (12, 16), interpolation=cv2.INTERSECT_NONE)
    img_exp[6:-6,8:-8] = img_preproc


    nbr = clf.predict(np.expand_dims(img_exp.flatten(), axis=0))[0]

    print(nbr)
    cv2.imshow('1', img_exp)
    cv2.waitKey()

    return nbr

def recognize_score(img):
    # Threshold the image
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    im_th = cv2.threshold(im_gray, 90, 255, cv2.THRESH_BINARY_INV)[1]
    for i in range(6):
        d = im_th[:,len(img[0])-i*10-8:len(img[0])-i*10]
        print(d.shape)
        digit = recognize_digit(d)

clf = joblib.load("digits_cls2.pkl")
recognize_score(cv2.imread('numbers.jpg'))