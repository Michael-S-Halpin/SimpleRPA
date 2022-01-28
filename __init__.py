import Delays
from Keyboard import *
from Mouse import *
from Screen import *
from Delays import *


def test_mouse():
    #mc = MouseConfig()
    #mc.log_screenshot = True
    #Mouse.move((70, 70), mc)
    #Mouse.down((70, 70))
    #Mouse.move((150, 70))
    #Mouse.up((150, 70))
    #Mouse.click(clicks=2)
    #mc.action_duration = 1
    #Mouse.drag((70,70), (150, 70), mc) # TODO: Not working Linux
    #time.sleep(3)
    #Mouse.scroll(-5)
    print()


def test_keyboard():
    #time.sleep(2)
    #Keyboard.press("Q")
    #Keyboard.press("a", CKeys.CTRL)
    #Keyboard.press("o", CKeys.ALT)
    #Keyboard.press("s", (CKeys.CTRL, CKeys.SHIFT))
    #Keyboard.press(CKeys.WIN) # Working Win TODO: WIN key not working?
    #Keyboard.type("this is a test")
    #Keyboard.type("a", CKeys.CTRL)
    #Keyboard.type("s", (CKeys.CTRL, CKeys.SHIFT))
    print()


def test_screen():
    #c1 = Screen.get_pixel_color((33, 112))
    #c2 = Screen.get_known_color((33, 112))
    #c3 = Screen.get_console_color((33, 112))
    #image = Screen.capture((0, 0, 128, 128))
    #Screen.capture_to_file((0,0,128,128), "test.bmp")
    #loc = Screen.find_image('/home/michaelhalpin/PycharmProjects/SimpleRPA/Folder.png')
    print()


def test_delays():
    #Delays.wait(2)
    #c = Screen.get_pixel_color((32,32))
    #z1 = Delays.wait_for_color((32,32), c)
    #z2 = Delays.wait_for_color((32,32), (0,0,0))
    #c = DelayConfig()
    #c.threshold = .95
    #f = '/home/michaelhalpin/PycharmProjects/SimpleRPA/Folder.png'
    #z1 = Delays.wait_for_image((0,0), f, c)
    #Delays.wait_for_change((0,0,100,100))
    print("")

#test_mouse()
#test_keyboard()
#test_screen()
test_delays()