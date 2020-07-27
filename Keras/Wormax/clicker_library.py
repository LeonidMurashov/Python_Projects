
import win32api as wapi
import win32api, win32con
from win32con import VK_MENU
from PIL import ImageGrab
import numpy as np


# Citation: Box Of Hats (https://github.com/Box-Of-Hats )
keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    keyList.append(char)


def get_keys():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)

    if wapi.GetAsyncKeyState(VK_MENU):
        keys.append("ALT")
    return keys
 

def mouse_down(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)


def mouse_up(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def get_screen():
    return np.array(ImageGrab.grab())
