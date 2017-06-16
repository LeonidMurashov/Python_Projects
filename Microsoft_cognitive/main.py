import requests, json
from PIL import Image,ImageDraw
f_path = "D://493ff96a99fa3.jpg"
file = open(f_path, "rb")
content = file.read()

result = requests.post("https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize", data=content,
                       headers={"Content-Type": "application/octet-stream",
                                "Ocp-Apim-Subscription-Key": "56dfe2baec16402ebe8cc635ac80838e"})
print(result.text)
face_result = json.loads(result.text)
image = Image.open(f_path)
draw = ImageDraw.Draw(image)
for f in face_result:
    face = f["faceRectangle"]
    draw.rectangle([(face["left"], face["top"]), (face["left"]+face["width"], face["top"]+face["height"])])
image.show()