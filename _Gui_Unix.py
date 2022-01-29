import os
from time import sleep
from Screen import *
from Mouse import *
from Keyboard import *

#TODO: Convert image files to a json format that includes a configuration object.
#TODO: Make constructor in platform convergence determine which library is loaded per instance.

# noinspection PyMethodMayBeStatic
class Application():
    app = None

    def __iter__(self):
        """Raise to avoid infinite loops"""
        raise NotImplementedError("Object is not iterable, try to use .windows()")

    def __getitem__(self, index):

        if index is None or index == '':
            return self

        pt = Application._get_center(Screen.find_image(index))
        Mouse.click(pt)
        return self

    def __getattribute__(self, attr_name):
        return object.__getattribute__(self, attr_name)

    def start(self, path):
        self.app = os.popen(path).detach()
        sleep(.5)
        return self

    def menu_select(self, paths):
        for path in paths:
            pt = Application._get_center(Screen.find_image(path))
            Mouse.click(pt)
            sleep(.2)

    def click(self):
        sleep(0)

    def type_keys(self, text, with_spaces = True):
        Keyboard.type_keys(text)

    @staticmethod
    def _get_center(rct):
        x = int((rct[0][2] / 2) + rct[0][0])
        y = int((rct[0][3] / 2) + rct[0][1])
        return x, y