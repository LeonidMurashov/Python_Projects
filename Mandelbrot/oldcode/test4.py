import pylab
import numpy as np


def _print_event(event, attr_list):
    print()
    print('**** {} ****'.format(event.name))
    print('    ' + str(type(event)))
    for attr in attr_list:
        title = 'event.' + attr
        value = getattr(event, attr)
        line = '    {title:20}: {value}'.format(title=title, value=value)
        print(line)


def onMouseEvent(event):
    # type: (matplotlib.backend_bases.MouseEvent) -> None
    '''
    Обработчик событий, связанных с мышью
    '''
    attr_list = ['name',
                 'dblclick', 'button', 'key',
                 'xdata', 'ydata',
                 'x', 'y',
                 'inaxes',
                 'step',
                 'guiEvent']
    print(event.inaxes)
    _print_event(event, attr_list)


def onKeyEvent(event):
    # type: (matplotlib.backend_bases.KeyEvent) -> None
    '''
    Обработчик событий, связанных с клавиатурой
    '''
    attr_list = ['name',
                 'key',
                 'xdata', 'ydata',
                 'x', 'y',
                 'inaxes',
                 'guiEvent']
    _print_event(event, attr_list)


if __name__ == '__main__':
    # Расчитываем функцию
    x = np.arange(0, 5 * np.pi, 0.01)
    y = np.sin(x) * np.cos(3 * x)

    # Нарисовать график
    fig = pylab.figure()
    pylab.plot(x, y)

    # События, связанные с мышью
    button_press_event_id = fig.canvas.mpl_connect('button_press_event',
                                                   onMouseEvent)

    button_release_event_id = fig.canvas.mpl_connect('button_release_event',
                                                     onMouseEvent)

    scroll_event_id = fig.canvas.mpl_connect('scroll_event',
                                             onMouseEvent)

    # События, связанные с клавишами
    key_press_event_id = fig.canvas.mpl_connect('key_press_event',
                                                onKeyEvent)

    key_release_event_id = fig.canvas.mpl_connect('key_release_event',
                                                  onKeyEvent)

    pylab.show()

    # Отпишемся от событий
    fig.canvas.mpl_disconnect(button_press_event_id)
    fig.canvas.mpl_disconnect(button_release_event_id)
    fig.canvas.mpl_disconnect(scroll_event_id)
    fig.canvas.mpl_disconnect(key_press_event_id)
    fig.canvas.mpl_disconnect(key_release_event_id)