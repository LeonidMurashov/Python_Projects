import wave,struct

#открываем файл для чтения
minus = wave.open("minus3.wav", mode="rb")
music = wave.open("music3.wav", mode="rb")
#создаем новый файл, в который будем писать
result = wave.open("voice.wav", mode="wb")

#берем параметры аудиопотока исходного файла (число каналов, част. дискр, глубина и тд.)
params = music.getparams()
#и задаем для нового такие же
result.setparams(params)

nframes = music.getnframes()
frames1 = minus.readframes(nframes)
frames2 = music.readframes(nframes)
minus_data = struct.unpack("<"+str(int(len(frames1)/2))+"h", frames1)
music_data = struct.unpack("<"+str(int(len(frames2)/2))+"h", frames2)
newdata = []

bias = 0
minErr = 32767*1000000
'''
for i in range(1000000,10):
	err = 0
	for j in range(0,10000,100):
		err += music_data[int(j + (i - 1000000/2))] - minus_data[j]
	if minErr > err:
		minErr = err
		bias = int(i - 1000000/2)
'''

def get_result(a,b):
	if abs(abs(a)-abs(b)) < 1000:
		return 0
	else:
		return abs(a)-abs(b)

try:
	i = 0
	while True:
		newdata.append(min(max((get_result(music_data[i],minus_data[i])), -32768),32767))
		i += 1
except:
	pass
newframes = struct.pack("<"+str(int(len(newdata)))+"h", *newdata)

result.writeframes(newframes)