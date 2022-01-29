import sys


class Window:
    gui = None
    app = None

    def __init__(self, use_api=True):
        if use_api:
            if sys.platform != "win32":
                import _Gui_Img as gui
            else:
                import _Gui_Api as gui
        else:
            import _Gui_Img as gui
        self.gui = gui

    def __iter__(self):
        """Raise to avoid infinite loops"""
        raise NotImplementedError("Object is not iterable, try to use .windows()")

    def __getitem__(self, index):
        return self.app[index]

    def __getattribute__(self, attr_name):
        return object.__getattribute__(self, attr_name)

    def start(self, path):
        self.app = self.gui.Application().start(path)
