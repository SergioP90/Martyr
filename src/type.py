import time
import pyautogui as pygui
import random as rand


def type_strokes(stroke_list, min_wait=0.05, max_wait=0.2):
    for key in stroke_list:
        if key == 'backspace':
            pygui.press('backspace')
        else:
            pygui.write(key)
        time.sleep(rand.uniform(min_wait, max_wait))