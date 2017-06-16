# Citation: Box Of Hats (https://github.com/Box-Of-Hats )

import win32api as wapi
from win32con import VK_MENU
import time

keyList = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    if wapi.GetAsyncKeyState(VK_MENU):
        keys.append("ALT")
    return keys