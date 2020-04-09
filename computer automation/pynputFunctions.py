from pynput.keyboard import Key, Controller
import pynput
import pandas as pd
import re 
import subprocess
import time

#example of of to press keys
keyboard = Controller()
keyboard.press('a')
keyboard.release('a')

keyboard.press(Key.ctrl)
keyboard.press('c')
keyboard.release('c')
keyboard.release(Key.ctrl)

keyboard.type('Nitratine')
# This method does also support spaces but when it comes to enters, use a new line character (\n) and a tab character (\t) for tabs.


#useful functions I've made
dateIndex = pd.date_range(start='1/1/2020', end='3/13/2020')

#I probably could just use keyboard.type instead, but oh well
def pressAndRelease(keyboardValue):
    if isinstance(keyboardValue,str):
        for st in keyboardValue:
            keyboard.press(st)
            keyboard.release(st)
            time.sleep(0.1)
    else:
        keyboard.press(keyboardValue)
        keyboard.release(keyboardValue)
    time.sleep(0.5)

def holdSpecialKeyPressKey(specialKey, stringValue):
    keyboard.press(specialKey)
    pressAndRelease(stringValue)
    keyboard.release(specialKey)
    time.sleep(0.5)




#Mouse control examples

from pynput.mouse import Button, Controller

mouse = Controller()

# Read pointer position
print('The current pointer position is {0}'.format(
    mouse.position))

# Set pointer position
mouse.position = (10, 20)
print('Now we have moved it to {0}'.format(
    mouse.position))

# Move pointer relative to current position
mouse.move(5, -5)

# Press and release
mouse.press(Button.left)
mouse.release(Button.left)

# Double click; this is different from pressing and releasing
# twice on Mac OSX
mouse.click(Button.left, 2)

# Scroll two steps down
mouse.scroll(0, 2)