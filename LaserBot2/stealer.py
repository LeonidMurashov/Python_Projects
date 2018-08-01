import urllib.request
f = urllib.request.urlopen("https://tanks.geekclass.ru/stats")
a = f.read()
print(a)
with open("site.txt", "w") as file:
	file.write(str(a))
	