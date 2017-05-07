
from PIL import Image
from pytesseract import image_to_string
import pytesseract

api = pytesseract.TessBaseAPI()
image_file = "D:/test.png"
im = Image.open(image_file)
text = image_to_string(im)
print "=====output=======\n"
print text