import urllib

import requests, json
from PIL import Image,ImageDraw
f_path = "D://493ff96a99fa3.jpg"
file = open(f_path, "rb")
content = file.read()

params = urllib.parse.urlencode({
    # Request parameters
    'visualFeatures': 'Categories',
    'details': '{string}',
    'language': 'en',
})

result = requests.post("https://westus.api.cognitive.microsoft.com/vision/v1/analyses", data=content,
                       headers={"Content-Type": "application/octet-stream",
                                "Ocp-Apim-Subscription-Key": "124d928e2dda44bf83ad4171fde8b99f"}, params=params)
print(result.text)
face_result = json.loads(result.text)
image = Image.open(f_path)
draw = ImageDraw.Draw(image)
for f in face_result:
    face = f["faceRectangle"]
    draw.rectangle([(face["left"], face["top"]), (face["left"]+face["width"], face["top"]+face["height"])])
image.show()