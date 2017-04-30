from __future__ import absolute_import, division, print_function
import time
from functools import partial
from threading import Thread
from Queue import Queue
import win32api
import win32con
from pynput.mouse import Listener
#http://stackoverflow.com/questions/40000353/mouse-recorder-how-to-detect-mouse-click-in-a-while-loop-with-win32api

isPressed = False

def on_click(x, y, button, pressed):
    global isPressed
    isPressed = pressed

def detect_clicks():
    with Listener(on_click=partial(on_click)) as listener:
        listener.join()


'''def track_movement(queue):
    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        x, y = win32api.GetCursorPos()
        print(x, y)
        queue.put('{0},{1}\n'.format(x, y))
        time.sleep(0.2)'''


def main():
    #thread.daemon = True
    thread = Thread(target=detect_clicks)
    thread.start()
    with open('log.txt', 'w') as log_file:
        while True:
            time.sleep(0)
            print(isPressed)


if __name__ == '__main__':
    main()