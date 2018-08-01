# -*- coding: UTF-8 -*-

import pylab
import numpy as np


marker = None


def onMouseClick(event):
    # type: (matplotlib.backend_bases.MouseEvent) -> None
    axes = event.inaxes

    # Если кликнули вне какого-либо графика, то не будем ничего делать
    if axes is None:
        return

    global marker
    # Если маркер с текстом уже был создан, то удалим его
    if marker is not None:
        marker.remove()

    # В качестве текущих выберем оси, внутри которых кликнули мышью
    pylab.sca(axes)

    # Координаты клика в системе координат осей
    x = event.xdata
    y = event.ydata
    text = u'({:.3f}; {:.3f})'.format(x, y)

    # Выведем текст в точку, куда кликнули
    marker = pylab.text(x, y, text)

    # Обновим график
    pylab.show()


if __name__ == '__main__':
    # Расчитываем функции
    x = np.arange(0, 5 * np.pi, 0.01)
    y1 = np.sin(x) * np.cos(3 * x)
    y2 = np.sin(x) * np.cos(5 * x)

    # Создадим окно с графиком
    fig = pylab.figure()

    # Нарисуем первый график
    pylab.subplot(2, 1, 1)
    pylab.plot(x, y1)
    pylab.grid()

    # Нарисуем второй график, cmap = mycmap
    pylab.subplot(2, 1, 2)
    pylab.plot(x, y2)
    pylab.grid()

    # Подписка на событие
    fig.canvas.mpl_connect('button_press_event', onMouseClick)

    pylab.show()