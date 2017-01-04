#github.com/roctbb/GoTo

import wave,struct

#открываем файл для чтения
source = wave.open("task1.wav", mode="rb")
#создаем новый файл, в который будем писать
result = wave.open("result1.wav", mode="wb")

#берем параметры аудиопотока исходного файла (число каналов, част. дискр, глубина и тд.)
params = source.getparams()
#и задаем для нового такие же
result.setparams(params)

nframes = source.getnframes()

data = struct.unpack("<"+str(nframes)+"h", source.readframes(nframes))
newdata = []

data.reverse()

for frame in data:
    newdata.append(frame*10)

newframes = struct.pack("<"+str(nframes)+"h", *newdata)

result.writeframes(newframes)