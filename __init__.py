import sys
import json
import time
from Keyboard import *
from Mouse import *
from Screen import *
from colorama import Fore


def test_mouse():
    mc = MouseConfig()
    #Mouse.move((70, 70))
    #Mouse.down((70, 70))
    #Mouse.move((150, 70))
    #Mouse.up((150, 70))
    #Mouse.click(clicks=2)
    #config = MouseConfig()
    #config.action_duration = 1
    #Mouse.drag((70,70), (150, 70), config) # TODO: Not working Linux
    #time.sleep(3)
    #Mouse.scroll(-5)
    #print()


def test_keyboard():
    time.sleep(3)
    #Keyboard.press("Q")
    #Keyboard.press("a", CKeys.CTRL)
    #Keyboard.press("o", CKeys.ALT)
    #Keyboard.press("s", (CKeys.CTRL, CKeys.SHIFT))
    #Keyboard.press(CKeys.WIN) # Working Win TODO: WIN key not working?
    #Keyboard.type("this is a test")
    #Keyboard.type("a", CKeys.CTRL)
    Keyboard.type("s", (CKeys.CTRL, CKeys.SHIFT))


def test_screen():
    #c1 = Screen.get_pixel_color((33, 112))
    #c2 = Screen.get_known_color((33, 112))
    #c3 = Screen.get_console_color((33, 112))
    #image = Screen.capture((0, 0, 128, 128))
    #Screen.capture_to_file((0,0,128,128), "test.bmp")
    loc = Screen.find_image('/home/michaelhalpin/PycharmProjects/SimpleRPA/icon.bmp')
    print()

#test_mouse()
#test_keyboard()
test_screen()