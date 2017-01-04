__author__ = 'roctbb'

import wave,struct

#открываем файл для чтения
source = wave.open("task1.wav", mode="rb")
#создаем новый файл, в который будем писать
result = wave.open("result1.wav", mode="wb")

#берем параметры аудиопотока исходного файла (число каналов, част. дискр, глубина и тд.)
params = source.getparams()
#и задаем для нового такие же
result.setparams(params)

#для каждого фрейма
for i in range(source.getnframes()):
    #читаем фрейм = два байта данных для 16битного 1 канального wav
    frame = source.readframes(1)
    #декодируем байты в число
    #команда unpack почему то возвращает пару элементов даже для моно, поэтому берем 0 элемент
    data = int(struct.unpack("<h", frame)[0])
    #увеличиваем амплитуду
    newdata = data*10
    #кодируем обратно в байты
    frame = struct.pack("<h", newdata)
    #записываем фрейм в новый файл
    result.writeframes(frame)
#закрываем файл
result.close()

#github.com/roctbb/goto/

