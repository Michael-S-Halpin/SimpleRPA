# region License
"""
 * SimplRPA - A simple RPA library for Python and C#
 *
 * This file has been forked from PyAutoGui https://github.com/asweigart/pyautogui
 *
 * Copyright (c) Al Sweigart
 * Modifications (c) as per Git change history
 * Modifications (c) 2021 Michael Halpin
 *
 * This Source Code Form is subject to the terms of the Mozilla
 * Public License, v. 2.0. If a copy of the MPL was not distributed
 * with this file, You can obtain one at
 * https://mozilla.org/MPL/2.0/.
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial
 * portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
 * LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
# endregion
from __future__ import absolute_import, division, print_function

import collections.abc
import datetime
import functools
import os
import platform
import re
import sys
import time
from contextlib import contextmanager

from Screen import Screen
from _Widget import Widget

collectionsSequence = collections.abc.Sequence  # type: ignore
version = "1.0"


# region CUSTOM EXCEPTIONS
class SimpleRPAException(Exception):
    """
    SimpleRPA code will raise this exception class for any invalid actions. If SimpleRPA raises some other exception,
    you should assume that this is caused by a bug in SimpleRPA itself. (Including a failure to catch potential
    exceptions raised by SimpleRPA.)
    """

    pass


class FailSafeException(SimpleRPAException):
    """
    This exception is raised by SimpleRPA functions when the user puts the mouse cursor into one of the "failsafe
    points" (by default, one of the four corners of the primary monitor). This exception shouldn't be caught; it's
    meant to provide a way to terminate a misbehaving script.
    """

    pass


class ImageNotFoundException(SimpleRPAException):
    """
    This exception is the SimpleRPA version of PyScreeze's `ImageNotFoundException`, which is raised when a locate*()
    function call is unable to find an image.
    Ideally, `pyscreeze.ImageNotFoundException` should never be raised by SimpleRPA.
    """
# endregion


# region IMPORT TWEANING
try:
    from pytweening import (
        easeInQuad,
        easeOutQuad,
        easeInOutQuad,
        easeInCubic,
        easeOutCubic,
        easeInOutCubic,
        easeInQuart,
        easeOutQuart,
        easeInOutQuart,
        easeInQuint,
        easeOutQuint,
        easeInOutQuint,
        easeInSine,
        easeOutSine,
        easeInOutSine,
        easeInExpo,
        easeOutExpo,
        easeInOutExpo,
        easeInCirc,
        easeOutCirc,
        easeInOutCirc,
        easeInElastic,
        easeOutElastic,
        easeInOutElastic,
        easeInBack,
        easeOutBack,
        easeInOutBack,
        easeInBounce,
        easeOutBounce,
        easeInOutBounce,
    )

    # getLine is not needed.
    # getPointOnLine has been redefined in this file, to avoid dependency on pytweening.
    # linear has also been redefined in this file.
except ImportError:

    # noinspection PyUnusedLocal
    def _could_not_import_py_tweening(*unused_args, **unused_kwargs):
        """
        This function raises ``SimpleRPAException``. It's used for the PyTweening function names if the PyTweening
        module failed to be imported.
        :return:
        """
        raise SimpleRPAException(
            "SimpleRPA was unable to import pytweening. Please install this module to enable the function you tried "
            "to call. "
        )


    # noinspection DuplicatedCode
    easeInQuad = _could_not_import_py_tweening
    easeOutQuad = _could_not_import_py_tweening
    easeInOutQuad = _could_not_import_py_tweening
    easeInCubic = _could_not_import_py_tweening
    easeOutCubic = _could_not_import_py_tweening
    easeInOutCubic = _could_not_import_py_tweening
    easeInQuart = _could_not_import_py_tweening
    easeOutQuart = _could_not_import_py_tweening
    easeInOutQuart = _could_not_import_py_tweening
    easeInQuint = _could_not_import_py_tweening
    easeOutQuint = _could_not_import_py_tweening
    easeInOutQuint = _could_not_import_py_tweening
    easeInSine = _could_not_import_py_tweening
    easeOutSine = _could_not_import_py_tweening
    easeInOutSine = _could_not_import_py_tweening
    # noinspection DuplicatedCode
    easeInExpo = _could_not_import_py_tweening
    easeOutExpo = _could_not_import_py_tweening
    easeInOutExpo = _could_not_import_py_tweening
    easeInCirc = _could_not_import_py_tweening
    easeOutCirc = _could_not_import_py_tweening
    easeInOutCirc = _could_not_import_py_tweening
    easeInElastic = _could_not_import_py_tweening
    easeOutElastic = _could_not_import_py_tweening
    easeInOutElastic = _could_not_import_py_tweening
    easeInBack = _could_not_import_py_tweening
    easeOutBack = _could_not_import_py_tweening
    easeInOutBack = _could_not_import_py_tweening
    easeInBounce = _could_not_import_py_tweening
    easeOutBounce = _could_not_import_py_tweening
    easeInOutBounce = _could_not_import_py_tweening
# endregion


def raise_simple_rpa_image_not_found_exception(wrapped_function):
    """
    A decorator that wraps PyScreeze locate*() functions so that the SimpleRPA user sees them raise SimpleRPA's
    ImageNotFoundException rather than PyScreeze's ImageNotFoundException. This is because PyScreeze should be
    invisible to SimpleRPA users.
    :param wrapped_function:
    :return:
    """

    @functools.wraps(wrapped_function)
    def wrapper(*args, **kwargs):
        try:
            return wrapped_function(*args, **kwargs)
        except pyscreeze.ImageNotFoundException:
            raise ImageNotFoundException  # Raise SimpleRPA's ImageNotFoundException.

    return wrapper


# region SCREEN SHOTS TODO: CAN WE JUST USE SCREEN.PY?
try:
    # noinspection PyUnresolvedReferences
    import pyscreeze
    from pyscreeze import center, grab, pixel, pixelMatchesColor, screenshot

    # Change the locate*() functions so that they raise SimpleRPA's ImageNotFoundException instead.
    @raise_simple_rpa_image_not_found_exception
    def locate(*args, **kwargs):
        return pyscreeze.locate(*args, **kwargs)


    locate.__doc__ = pyscreeze.locate.__doc__


    @raise_simple_rpa_image_not_found_exception
    def locate_all(*args, **kwargs):
        return pyscreeze.locateAll(*args, **kwargs)


    locate_all.__doc__ = pyscreeze.locateAll.__doc__


    @raise_simple_rpa_image_not_found_exception
    def locate_all_on_screen(*args, **kwargs):
        return pyscreeze.locateAllOnScreen(*args, **kwargs)


    locate_all_on_screen.__doc__ = pyscreeze.locateAllOnScreen.__doc__


    @raise_simple_rpa_image_not_found_exception
    def locate_center_on_screen(*args, **kwargs):
        return pyscreeze.locateCenterOnScreen(*args, **kwargs)


    locate_center_on_screen.__doc__ = pyscreeze.locateCenterOnScreen.__doc__


    @raise_simple_rpa_image_not_found_exception
    def locate_on_screen(*args, **kwargs):
        return pyscreeze.locateOnScreen(*args, **kwargs)


    locate_on_screen.__doc__ = pyscreeze.locateOnScreen.__doc__


    @raise_simple_rpa_image_not_found_exception
    def locate_on_window(*args, **kwargs):
        return pyscreeze.locateOnWindow(*args, **kwargs)


    locate_on_window.__doc__ = pyscreeze.locateOnWindow.__doc__


except ImportError:
    # If pyscreeze module is not found, screenshot-related features will simply not work.
    # noinspection PyUnusedLocal
    def _could_not_import_py_screeze(*unused_args, **unsed_kwargs):
        """
        This function raises ``SimpleRPAException``. It's used for the PyScreeze function names if the PyScreeze module
        failed to be imported.
        :return:
        """
        raise SimpleRPAException(
            "SimpleRPA was unable to import pyscreeze. (This is likely because you're running a version of Python that "
            "Pillow (which pyscreeze depends on) doesn't support currently.) Please install this module to enable the "
            "function you tried to call."
        )


    center = _could_not_import_py_screeze
    grab = _could_not_import_py_screeze
    locate = _could_not_import_py_screeze
    locateAll = _could_not_import_py_screeze
    locateAllOnScreen = _could_not_import_py_screeze
    locateCenterOnScreen = _could_not_import_py_screeze
    locateOnScreen = _could_not_import_py_screeze
    locateOnWindow = _could_not_import_py_screeze
    pixel = _could_not_import_py_screeze
    pixelMatchesColor = _could_not_import_py_screeze
    screenshot = _could_not_import_py_screeze
# endregion


# region IMPORTS MOUSE INFO TODO: Another thing we can get rid of eventually.
try:
    # noinspection PyUnresolvedReferences
    import mouseinfo


    def mouse_info():
        """
        Launches the MouseInfo app. This application provides mouse coordinate information which can be useful when
        planning GUI automation tasks. This function blocks until the application is closed.
        :return:
        """
        mouseinfo.MouseInfoWindow()


except ImportError:

    def mouse_info():
        """
        This function raises SimpleRPAException. It's used for the MouseInfo function names if the MouseInfo module
        failed to be imported.
        :return:
        """
        raise SimpleRPAException(
            "SimpleRPA was unable to import mouseinfo. Please install this module to enable the function you "
            "tried to call. "
        )


# endregion


if sys.platform == "win32":  # PyGetWindow currently only supports Windows.
    try:
        from pygetwindow import (
            Window,
            getActiveWindow,
            getActiveWindowTitle,
            getWindowsAt,
            getWindowsWithTitle,
            getAllWindows,
            getAllTitles,
        )
    except ImportError:
        # If pygetwindow module is not found, those methods will not be available.
        # noinspection PyUnusedLocal
        def _could_not_import_py_get_window(*unused_args, **unused_kwargs):
            """
            This function raises SimpleRPAException. It's used for the PyGetWindow function names if the PyGetWindow
            module failed to be imported.
            """
            raise SimpleRPAException(
                "SimpleRPA was unable to import pygetwindow. Please install this module to enable the function you "
                "tried to call. "
            )


        Window = _could_not_import_py_get_window
        getActiveWindow = _could_not_import_py_get_window
        getActiveWindowTitle = _could_not_import_py_get_window
        getWindowsAt = _could_not_import_py_get_window
        getWindowsWithTitle = _could_not_import_py_get_window
        getAllWindows = _could_not_import_py_get_window
        getAllTitles = _could_not_import_py_get_window

# region CONSTANTS
KEY_NAMES = [
    "\t",
    "\n",
    "\r",
    " ",
    "!",
    '"',
    "#",
    "$",
    "%",
    "&",
    "'",
    "(",
    ")",
    "*",
    "+",
    ",",
    "-",
    ".",
    "/",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    ":",
    ";",
    "<",
    "=",
    ">",
    "?",
    "@",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "`",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
    "accept",
    "add",
    "alt",
    "altleft",
    "altright",
    "apps",
    "backspace",
    "browserback",
    "browserfavorites",
    "browserforward",
    "browserhome",
    "browserrefresh",
    "browsersearch",
    "browserstop",
    "capslock",
    "clear",
    "convert",
    "ctrl",
    "ctrlleft",
    "ctrlright",
    "decimal",
    "del",
    "delete",
    "divide",
    "down",
    "end",
    "enter",
    "esc",
    "escape",
    "execute",
    "f1",
    "f10",
    "f11",
    "f12",
    "f13",
    "f14",
    "f15",
    "f16",
    "f17",
    "f18",
    "f19",
    "f2",
    "f20",
    "f21",
    "f22",
    "f23",
    "f24",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "final",
    "fn",
    "hanguel",
    "hangul",
    "hanja",
    "help",
    "home",
    "insert",
    "junja",
    "kana",
    "kanji",
    "launchapp1",
    "launchapp2",
    "launchmail",
    "launchmediaselect",
    "left",
    "modechange",
    "multiply",
    "nexttrack",
    "nonconvert",
    "num0",
    "num1",
    "num2",
    "num3",
    "num4",
    "num5",
    "num6",
    "num7",
    "num8",
    "num9",
    "numlock",
    "pagedown",
    "pageup",
    "pause",
    "pgdn",
    "pgup",
    "playpause",
    "prevtrack",
    "print",
    "printscreen",
    "prntscrn",
    "prtsc",
    "prtscr",
    "return",
    "right",
    "scrolllock",
    "select",
    "separator",
    "shift",
    "shiftleft",
    "shiftright",
    "sleep",
    "space",
    "stop",
    "subtract",
    "tab",
    "up",
    "volumedown",
    "volumemute",
    "volumeup",
    "win",
    "winleft",
    "winright",
    "yen",
    "command",
    "option",
    "optionleft",
    "optionright",
]
KEYBOARD_KEYS = KEY_NAMES  # keeping old KEYBOARD_KEYS for backwards compatibility

# Constants for the mouse button names:
LEFT = "left"
MIDDLE = "middle"
RIGHT = "right"
PRIMARY = "primary"
SECONDARY = "secondary"

# Different keyboard mappings:
# TODO - finish this feature.
# NOTE: Eventually, I'd like to come up with a better system than this. For now, this seems like it works.
QWERTY = r"""`1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?"""
QWERTZ = r"""=1234567890/0qwertzuiop89-asdfghjkl,\yxcvbnm,.7+!@#$%^&*()?)QWERTZUIOP*(_ASDFGHJKL<|YXCVBNM<>&"""
# endregion

# region IMPORTS PLATFORM SPECIFIC RPA
if sys.platform == "darwin":
    # noinspection PyPep8Naming
    import _Rpa_OSX as platform_module
elif sys.platform == "win32":
    # noinspection PyPep8Naming
    import _Rpa_Win as platform_module
    import _Gui_Win as gui
elif platform.system() == "Linux":
    # noinspection PyPep8Naming
    import _Rpa_Linux as platform_module
else:
    raise NotImplementedError("Your platform (%s) is not supported by SimpleRPA." % (platform.system()))
# endregion

# region TWEAK-ABLE SETTINGS
# In seconds. Any duration less than this is rounded to 0.0 to instantly move the mouse.
MINIMUM_DURATION = 0.1

# If sleep_amount is less than MINIMUM_DURATION, time.sleep() will be a no-op and the mouse cursor moves there
# instantly. TODO: This value should vary with the platform. http://stackoverflow.com/q/1133857
MINIMUM_SLEEP = 0.05

# The number of seconds to pause after EVERY public function call. Useful for debugging:
PAUSE = 0.1  # Tenth-second pause by default.

# Interface need some catch up time on darwin (macOS) systems. Possible values probably differ based on your system
# performance. This value affects mouse moveTo, dragTo and key event duration. TODO: Find a dynamic way to let the
#  system catch up instead of blocking with a magic number.
DARWIN_CATCH_UP_TIME = 0.01

# If the mouse is over a coordinate in FAILSAFE_POINTS and FAILSAFE is True, the FailSafeException is raised. The
# rest of the points are added to the FAILSAFE_POINTS list at the bottom of this file, after size() has been defined.
# The points are for the corners of the screen, but note that these points don't automatically change if the screen
# resolution changes.
FAILSAFE = True
FAILSAFE_POINTS = [(0, 0)]

LOG_SCREENSHOTS = False  # If True, save screenshots for clicks and key presses.

# If not None, SimpleRPA deletes old screenshots when this limit has been reached:
LOG_SCREENSHOTS_LIMIT = 10
G_LOG_SCREENSHOTS_FILENAMES = []  # TODO - make this a deque
# endregion

Point = collections.namedtuple("Point", "x y")
Size = collections.namedtuple("Size", "width height")


# region GENERAL METHODS
def is_shift_character(character):
    """
    Returns True if the ``character`` is a keyboard key that would require the shift key to be held down, such as
    uppercase letters or the symbols on the keyboard's number row.
    :param character:
    :return:
    """

    # NOTE TODO - This will be different for non-qwerty keyboards.
    return character.isupper() or character in set('~!@#$%^&*()_+{}|:"<>?')


def _generic_simple_rpa_checks(wrapped_function):
    """
    A decorator that calls failSafeCheck() before the decorated function and _handlePause() after it.
    :param wrapped_function:
    :return:
    """

    @functools.wraps(wrapped_function)
    def wrapper(*args, **kwargs):
        fail_safe_check()
        return_val = wrapped_function(*args, **kwargs)
        _handle_pause(kwargs.get("_pause", True))
        return return_val

    return wrapper


def get_point_on_line(x1, y1, x2, y2, n):
    """
    Plots all tweening points along a line.
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :param n:
    :return: tuple
    """

    x = ((x2 - x1) * n) + x1
    y = ((y2 - y1) * n) + y1

    return x, y


def linear(n):
    """
    The default tween for all mouse functions.
    :param n:
    :return: float
    """
    # We use this function instead of pytweening.linear for the default tween function just in case pytweening
    # couldn't be imported.
    if not 0.0 <= n <= 1.0:
        raise SimpleRPAException("Argument must be between 0.0 and 1.0.")
    return n


def _handle_pause(_pause):
    """
    A helper function for performing a pause at the end of a SimpleRPA function based on some settings.
    :param _pause: If `_pause` is `True`, then sleep for `PAUSE` seconds (the global pause setting).
    :return: tuple
    """

    if _pause:
        assert isinstance(PAUSE, int) or isinstance(PAUSE, float)
        time.sleep(PAUSE)


# noinspection PyArgumentList
def _normalize_xy_args(first_arg, second_arg):
    """
    Returns a `Point` object based on `firstArg` and `secondArg`, which are the first two arguments passed to
    several SimpleRPA functions. If `firstArg` and `secondArg` are both `None`, returns the current mouse cursor
    position.
    :param first_arg:
    :param second_arg:
    :return: void
    """

    if first_arg is None and second_arg is None:
        return position()

    elif isinstance(first_arg, str):
        # If x is a string, we assume it's an image filename to locate on the screen:
        try:
            location = locateOnScreen(first_arg)
            # The following code only runs if pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION is not set to True, meaning that
            # locateOnScreen() returns None if the image can't be found.
            if location is not None:
                return center(location)

            else:
                return None

        except pyscreeze.ImageNotFoundException:
            raise ImageNotFoundException

    elif isinstance(first_arg, collectionsSequence):
        if len(first_arg) == 2:
            # firstArg is a two-integer tuple: (x, y)
            if second_arg is None:
                return Point(int(first_arg[0]), int(first_arg[1]))

            else:
                raise SimpleRPAException(
                    "When passing a sequence for firstArg, secondArg must not be passed (received {0}).".format(
                        repr(second_arg)
                    )
                )

        elif len(first_arg) == 4:
            # firstArg is a four-integer tuple, (left, top, width, height), we should return the center point
            if second_arg is None:
                return center(first_arg)

            else:
                raise SimpleRPAException(
                    "When passing a sequence for first_arg, second_arg must not be passed and default to None ("
                    "received {0}).".format(
                        repr(second_arg)
                    )
                )
        else:
            raise SimpleRPAException(
                "The supplied sequence must have exactly 2 or exactly 4 elements ({0} were received).".format(
                    len(first_arg)
                )
            )
    else:
        return Point(int(first_arg), int(second_arg))  # firstArg and secondArg are just x and y number values


def _log_screenshot(log_screenshot, func_name, func_args, folder="."):
    """
    A helper function that creates a screenshot to act as a logging mechanism. When a SimpleRPA function is called,
    this function is also called to capture the state of the screen when that function was called.
    :param log_screenshot: If this is `False` (or None and the `LOG_SCREENSHOTS` constant is `False`), no screenshot
    is taken.
    :param func_name: This argument is a string of the calling function's name. It's used in the screenshot's filename.
    :param func_args: This argument is a string describing the arguments passed to the calling function. It's limited
    to twelve characters to keep it short.
    :param folder: This argument is the folder to place the screenshot file in, and defaults to the current
    working directory.
    :return: tuple
    """

    if not log_screenshot:
        return  # Don't take a screenshot.

    if log_screenshot is None and not LOG_SCREENSHOTS:
        return  # Don't take a screenshot.

    # Ensure that the "specifics" string isn't longer than the max length for a filename:
    if len(func_args) > 12:
        func_args = func_args[:12] + "..."

    now = datetime.datetime.now()
    filename = "%s-%s-%s_%s-%s-%s-%s_%s_%s.png" % (
        now.year,
        str(now.month).rjust(2, "0"),
        str(now.day).rjust(2, "0"),
        now.hour,
        now.minute,
        now.second,
        str(now.microsecond)[:3],
        func_name,
        func_args,
    )

    filepath = os.path.join(folder, filename)

    # Delete the oldest screenshot if we've reached the maximum:
    if (LOG_SCREENSHOTS_LIMIT is not None) and (len(G_LOG_SCREENSHOTS_FILENAMES) >= LOG_SCREENSHOTS_LIMIT):
        os.unlink(os.path.join(folder, G_LOG_SCREENSHOTS_FILENAMES[0]))
        del G_LOG_SCREENSHOTS_FILENAMES[0]

    pt = Widget.get_screen_resolution()
    Screen.capture_to_file((0, 0, pt[0], pt[1]), filepath)
    G_LOG_SCREENSHOTS_FILENAMES.append(filename)


# noinspection PyArgumentList,PyProtectedMember
def position(x=None, y=None):
    """
    Returns the current xy coordinates of the mouse cursor as a two-integer tuple.
    :param x: If not None, this argument overrides the x in the return value.
    :param y: If not None, this argument overrides the y in the return value.
    :return: tuple
    """

    pos_x, posy = platform_module._position()
    pos_x = int(pos_x)
    posy = int(posy)

    if x is not None:  # If set, the x parameter overrides the return value.
        pos_x = int(x)

    if y is not None:  # If set, the y parameter overrides the return value.
        posy = int(y)

    return Point(pos_x, posy)


# noinspection PyProtectedMember
def size():
    """
    Returns the width and height of the screen as a two-integer tuple.
    :return: tuple
    """
    return Size(*platform_module._size())


# noinspection PyProtectedMember
def on_screen(x, y=None):
    """
    Returns whether the given xy coordinates are on the primary screen or not.
    Note that this function doesn't work for secondary screens.
    :param x: The x position of the mouse event.
    :param y: The y position of the mouse event.
    :return: void
    """
    x, y = _normalize_xy_args(x, y)
    x = int(x)
    y = int(y)

    width, height = platform_module._size()
    return 0 <= x < width and 0 <= y < height
# endregion


# region MOUSE METHODS
"""
NOTE: Although "mouse1" and "mouse2" buttons usually refer to the left and
right mouse buttons respectively, in SimpleRPA 1, 2, and 3 refer to the left,
middle, and right buttons, respectively. This is because Xlib interprets
button 2 as the middle button and button 3 as the right button, so we hold
that for Windows and macOS as well (since those operating systems don't use
button numbers but rather just "left" or "right").
"""


def _normalize_button(button):
    """
    The left, middle, and right mouse buttons are button numbers 1, 2, and 3 respectively. This is the numbering that
    Xlib on Linux uses (while Windows and macOS don't care about numbers; they just use "left" and "right").
    This function takes one of ``LEFT``, ``MIDDLE``, ``RIGHT``, ``PRIMARY``, ``SECONDARY``, ``1``, ``2``, ``3``, ``4``,
    ``5``, ``6``, or ``7`` for the button argument and returns either ``LEFT``, ``MIDDLE``, ``RIGHT``, ``4``, ``5``,
    ``6``, or ``7``. The ``PRIMARY``, ``SECONDARY``, ``1``, ``2``, and ``3`` values are never returned.
    The ``'left'`` and ``'right'`` mouse buttons will always refer to the physical left and right
    buttons on the mouse. The same applies for buttons 1 and 3.
    However, if ``button`` is ``'primary'`` or ``'secondary'``, then we must check if
    the mouse buttons have been "swapped" (for left-handed users) by the operating system's mouse
    settings.
    If the buttons are swapped, the primary button is the right mouse button and the secondary button is the left mouse
    button. If not swapped, the primary and secondary buttons are the left and right buttons, respectively.
    NOTE: Swap detection has not been implemented yet.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :return: void
    """

    # TODO - The swap detection hasn't been done yet. For Windows,
    # see https://stackoverflow.com/questions/45627956/check-if-mouse-buttons-are-swapped-or-not-in-c TODO - We
    # should check the OS settings to see if it's a left-hand setup, where button 1 would be "right".

    # Check that `button` has a valid value:
    button = button.lower()
    if platform.system() == "Linux":
        # Check for valid button arg on Linux:
        if button not in (LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY, 1, 2, 3, 4, 5, 6, 7):
            raise SimpleRPAException("button argument must be one of ('left', 'middle', 'right', 'primary', "
                                     "'secondary', 1, 2, 3, 4, 5, 6, 7) ")
    else:
        # Check for valid button arg on Windows and macOS:
        if button not in (LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY, 1, 2, 3):
            raise SimpleRPAException(
                "button argument must be one of ('left', 'middle', 'right', 'primary', 'secondary', 1, 2, 3)"
            )

    # TODO - Check if the primary/secondary mouse buttons have been swapped:
    if button in (PRIMARY, SECONDARY):
        swapped = False  # TODO - Add the operating system-specific code to detect mouse swap later.
        if swapped:
            if button == PRIMARY:
                return RIGHT
            elif button == SECONDARY:
                return LEFT
        else:
            if button == PRIMARY:
                return LEFT
            elif button == SECONDARY:
                return RIGHT

    # Return a mouse button integer value, not a string like 'left':
    return {LEFT: LEFT, MIDDLE: MIDDLE, RIGHT: RIGHT, 1: LEFT, 2: MIDDLE, 3: RIGHT, 4: 4, 5: 5, 6: 6, 7: 7}[button]


# noinspection PyProtectedMember
@_generic_simple_rpa_checks
def mouse_down(x=None, y=None, button=PRIMARY, tween=linear, log_screenshot=None, pause=0):
    """
    Send the mouse down event to the operating system.
    :param x: The x position of the mouse event.
    :param y: The y position of the mouse event.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :return: void
    """

    button = _normalize_button(button)
    x, y = _normalize_xy_args(x, y)

    mouse_move_drag("move", x, y, x, y, duration=0, tween=tween)

    _log_screenshot(log_screenshot, "mouseDown", "%s,%s" % (x, y), folder=".")
    platform_module._mouse_down(x, y, button)

    if pause > 0:
        time.sleep(pause)


# noinspection PyProtectedMember
@_generic_simple_rpa_checks
def mouse_up(x=None, y=None, button=PRIMARY, tween=linear, log_screenshot=None, _pause=True):
    """
    Send the mouse up event to the operating system.
    :param x: The x position of the mouse event.
    :param y: The y position of the mouse event.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :return: void
    """

    button = _normalize_button(button)
    x, y = _normalize_xy_args(x, y)

    mouse_move_drag("move", x, y, x, y, duration=0, tween=tween)

    _log_screenshot(log_screenshot, "mouseUp", "%s,%s" % (x, y), folder=".")
    platform_module._mouse_up(x, y, button)


# noinspection PyProtectedMember
@_generic_simple_rpa_checks
def click(
        x=None, y=None, clicks=1, interval=0.0, button=PRIMARY, duration=0.0, tween=linear, log_screenshot=None,
        _pause=True
):
    """
    Clicks the specified button the specified number of times in the specified location.
    :param x: The x position of the mouse to click at.
    :param y: The y position of the mouse to click at.
    :param clicks: The number of clicks to make.
    :param interval: The time to wait between clicks.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :param duration: The total amount of time the operation should take.
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :return: void
    """

    # TODO: I'm leaving buttons 4, 5, 6, and 7 undocumented for now. I need to understand how they work.
    button = _normalize_button(button)
    x, y = _normalize_xy_args(x, y)

    # Move the mouse cursor to the x, y coordinate:
    mouse_move_drag("move", x, y, x, y, duration, tween)

    _log_screenshot(log_screenshot, "click", "%s,%s,%s,%s" % (button, clicks, x, y), folder=".")

    if sys.platform == 'darwin':
        for i in range(clicks):
            fail_safe_check()
            if button in (LEFT, MIDDLE, RIGHT):
                platform_module._multiclick(x, y, button, 1, interval)
    else:
        for i in range(clicks):
            fail_safe_check()
            if button in (LEFT, MIDDLE, RIGHT):
                platform_module._click(x, y, button)

            time.sleep(interval)


# noinspection PyProtectedMember
@_generic_simple_rpa_checks
def scroll(clicks, x=None, y=None, log_screenshot=None, pause=0):
    """
    Performs a scroll of the mouse scroll wheel.
    Whether this is a vertical or horizontal scroll depends on the underlying
    operating system.
    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.
    :param clicks: The amount of scrolling to do. A positive value is the mouse wheel moving forward (scrolling up),
    a negative value is backwards (down).
    :param x: The x position of the mouse event.
    :param y: The y position of the mouse event.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :return: void
    """

    if type(x) in (tuple, list):
        x, y = x[0], x[1]
    x, y = position(x, y)

    _log_screenshot(log_screenshot, "scroll", "%s,%s,%s" % (clicks, x, y), folder=".")
    platform_module._scroll(clicks, x, y)

    if pause > 0:
        time.sleep(pause)


@_generic_simple_rpa_checks
def move_to(x=None, y=None, duration=0.0, tween=linear, log_screenshot=False, _pause=True):
    """
    Moves the mouse cursor to a point on the screen.
    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.
    :param x: The x position on the screen where the click happens. None by default. If tuple, this is used for x and y.
    If x is a str, it's considered a filename of an image to find on the screen with locateOnScreen() and click
    the center of.
    :param y: The y position on the screen where the click happens. None by default.
    :param duration: The amount of time the operation should take to complete.
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :return: void
    """

    x, y = _normalize_xy_args(x, y)

    _log_screenshot(log_screenshot, "moveTo", "%s,%s" % (x, y), folder=".")
    mouse_move_drag("move", x, y, x, y, duration, tween)


@_generic_simple_rpa_checks
def drag_to(
        x=None, y=None, duration=0.0, tween=linear, button=PRIMARY, log_screenshot=None, _pause=True, mouse_down_up=True
):
    """
    Performs a mouse drag (mouse movement while a button is held down) to a
    point on the screen.
    The x and y parameters detail where the mouse event happens. If None, the
    current mouse position is used. If a float value, it is rounded down. If
    outside the boundaries of the screen, the event happens at edge of the
    screen.
    :param x: The x point on the screen to move to and mouse down from.
    :param y: The y point on the screen to move to and mouse down from.
    :param button: The mouse button, either 'left', 'middle', or 'right'
    :param duration: The amount of time the operation should take to complete.
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param button: The mouse button press and release.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :param mouse_down_up: When true, the mouseUp/Down actions are not performed. Which allows dragging over multiple
    (small) actions. 'True' by default.
    :return: void
    """

    x, y = _normalize_xy_args(x, y)
    _log_screenshot(log_screenshot, "dragTo", "%s,%s" % (x, y), folder=".")

    if mouse_down_up:
        mouse_down(button=button, logScreenshot=False, _pause=False)

    mouse_move_drag("drag", x, y, x, y, duration, tween, button)

    if mouse_down_up:
        mouse_up(button=button, logScreenshot=False, _pause=False)


# noinspection PyProtectedMember
def mouse_move_drag(move_or_drag, x1, y1, x2, y2, duration, tween=linear, button=LEFT, log_screenshot=False):
    """
    Handles the actual move or drag event, since different platforms
    implement them differently.
    On Windows & Linux, a drag is a normal mouse move while a mouse button is
    held down. On OS X, a distinct "drag" event must be used instead.
    The code for moving and dragging the mouse is similar, so this function
    handles both. Users should call the moveTo() or dragTo() functions instead
    of calling _mouseMoveDrag().
    :param move_or_drag: Either 'move' or 'drag', for the type of action this is.
    :param x1: The first x point on the screen to move to and mouse down from.
    :param y1: The first y point on the screen to move to and mouse down from.
    :param x2: The second x point on the screen to move to and mouse down from.
    :param y2: The second y point on the screen to move to and mouse down from.
    :param duration: The amount of time the operation should take to complete.
    :param tween: The tweening function used if the duration is not 0. A linear tween is used by default.
    :param button: The mouse button press and release.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :return: void
    """

    # The move and drag code is similar, but OS X requires a special drag event instead of just a move event
    # when dragging. See https://stackoverflow.com/a/2696107/1893164
    assert move_or_drag in ("move", "drag"), "moveOrDrag must be in ('move', 'drag'), not %s" % move_or_drag
    duration = duration / 2

    move_or_drag = move_or_drag
    if sys.platform == "darwin":
        move_or_drag = "osx_move"  # Only OS X needs the drag event specifically.

    start_x, start_y = position()
    width, height = size()

    # Make sure x and y are within the screen bounds.
    # x = max(0, min(x, width - 1))
    # y = max(0, min(y, height - 1))

    # If the duration is small enough, just move the cursor there instantly.
    steps = [(x1, y1)]

    if duration > MINIMUM_DURATION:
        # Non-instant moving/dragging involves tweening:
        num_steps = max(width, height)
        sleep_amount = duration / num_steps
        if sleep_amount < MINIMUM_SLEEP:
            num_steps = int(duration / MINIMUM_SLEEP)
            sleep_amount = duration / num_steps

        steps = [get_point_on_line(start_x, start_y, x1, y1, tween(n / num_steps)) for n in range(num_steps)]
        # Making sure the last position is the actual destination.
        steps.append((x2, y2))

    idx = 0
    for tween_x, tween_y in steps:
        idx += 1
        if len(steps) > 1:
            # A single step does not require tweening.
            # noinspection PyUnboundLocalVariable
            time.sleep(sleep_amount)

        tween_x = int(round(tween_x))
        tween_y = int(round(tween_y))

        # Do a fail-safe check to see if the user moved the mouse to a fail-safe position, but not if the mouse cursor
        # moved there as a result of this function. (Just because tweenX and tween_y aren't in a fail-safe position
        # doesn't mean the user couldn't have moved the mouse cursor to a fail-safe position.)
        if (tween_x, tween_y) not in FAILSAFE_POINTS:
            fail_safe_check()

        if move_or_drag == "move":
            platform_module._move_to(tween_x, tween_y)
        elif move_or_drag == "drag":
            platform_module._move_to(tween_x, tween_y)
            if idx == len(steps) - 1:
                platform_module._move_to(x1, y1)
                mouse_down(x1, y1, button, tween, log_screenshot, True)
                move_to(x2, y2, duration / 2, tween, log_screenshot, True)
                mouse_up(x2, y2, button, tween, log_screenshot, True)
        elif move_or_drag == "osx_drag":
            platform_module._drag_to(tween_x, tween_y, button)
        else:
            raise NotImplementedError("Unknown value of moveOrDrag: {0}".format(move_or_drag))

    _log_screenshot(log_screenshot, "moveTo", "%s,%s-%s,%s" % (x1, y1, x2, y2), folder=".")
    # noinspection PyUnboundLocalVariable
    if (tween_x, tween_y) not in FAILSAFE_POINTS:
        fail_safe_check()
# endregion


# region KEYBOARD METHODS
# noinspection PyProtectedMember
@_generic_simple_rpa_checks
def key_down(key, log_screenshot=None, _pause=True):
    """
    Performs a keyboard key press without the release. This will put that key in a held down state.
    :param key: The key to be pressed down. The valid names are listed in KEYBOARD_KEYS.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :return: void
    """

    if len(key) > 1:
        key = key.lower()

    _log_screenshot(log_screenshot, "keyDown", key, folder=".")
    platform_module._key_down(key)


# noinspection PyProtectedMember
@_generic_simple_rpa_checks
def key_up(key, log_screenshot=None, _pause=True):
    """
    Performs a keyboard key release (without the press down beforehand).
    :param key: The key to be released up. The valid names are listed in KEYBOARD_KEYS.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param _pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :return: void
    """

    if len(key) > 1:
        key = key.lower()

    _log_screenshot(log_screenshot, "keyUp", key, folder=".")
    platform_module._key_up(key)


# noinspection DuplicatedCode,PyProtectedMember
@_generic_simple_rpa_checks
def press(keys, presses=1, interval=0.0, log_screenshot=None, pause=0):
    """
    Performs a keyboard key press down, followed by a release.
    :param keys: The key to be pressed. The valid names are listed in KEYBOARD_KEYS. Can also be a list of such strings.
    :param presses: The number of press repetitions. 1 by default, for just one press.
    :param interval: How many seconds between each press. 0.0 by default, for no pause between presses.
    :param log_screenshot: If true a screenshot is taken during the operation.
    :param pause: How many seconds in the end of function process. None by default, for no pause in the end of
    function process.
    :return: void
    """

    if type(keys) == str:
        if len(keys) > 1:
            keys = keys.lower()
        keys = [keys]  # If keys is 'enter', convert it to ['enter'].
    else:
        lower_keys = []
        for s in keys:
            if len(s) > 1:
                lower_keys.append(s.lower())
            else:
                lower_keys.append(s)
        keys = lower_keys

    interval = float(interval)
    _log_screenshot(log_screenshot, "press", ",".join(keys), folder=".")

    for i in range(presses):
        for k in keys:
            fail_safe_check()
            platform_module._key_down(k)
            platform_module._key_up(k)
        time.sleep(interval)

    if pause > 0:
        time.sleep(pause)


@_generic_simple_rpa_checks
def typewrite(message, interval=0.0, log_screenshot=None, pause=0):
    """
    Performs a keyboard key press down, followed by a release, for each of the characters in message.
    The message argument can also be list of strings, in which case any valid keyboard name can be used.
    Since this performs a sequence of keyboard presses and does not hold down keys, it cannot be used to perform
    keyboard shortcuts. Use the hotkey() function for that.
    :param message: If a string, then the characters to be pressed. If a list, then the key names of the keys to press
    in order. The valid names are listed in KEYBOARD_KEYS.
    :param interval: The number of seconds in between each press. 0.0 by default, for no pause in between presses.
    :param log_screenshot: If true takes a screenshot during the operation.
    :param pause:
    :return: void
    """

    interval = float(interval)  # TODO - this should be taken out.

    _log_screenshot(log_screenshot, "write", message, folder=".")
    for c in message:
        if len(c) > 1:
            c = c.lower()
        press(c)
        time.sleep(interval)
        fail_safe_check()

    if pause > 0:
        time.sleep(pause)
# endregion


# region INTERNAL METHODS
def fail_safe_check():
    """
    Check to see if the mouse is in any of hte failsafe points. If so raise an exception to abort the process.
    :return: void
    """

    if FAILSAFE and tuple(position()) in FAILSAFE_POINTS:
        raise FailSafeException(
            "SimpleRPA fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set "
            "SimpleRPA.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED."
        )


def _get_number_token(command_str):
    """
    Gets the number token at the start of command_str.
    Given '5hello' returns '5'
    Given '  5hello' returns '  5'
    Given '-42hello' returns '-42'
    Given '+42hello' returns '+42'
    Given '3.14hello' returns '3.14'
    Raises an exception if it can't tokenize a number.
    :param command_str:
    :return:
    """

    # noinspection RegExpSingleCharAlternation,RegExpRedundantEscape
    pattern = re.compile(r"^(\s*(\+|\-)?\d+(\.\d+)?)")
    mo = pattern.search(command_str)
    if mo is None:
        raise SimpleRPAException("Invalid command at index 0: a number was expected")

    return mo.group(1)


def _get_quoted_string_token(command_str):
    """
    Gets the quoted string token at the start of command_str. The quoted string must use single quotes.
    Given "'hello'world" returns "'hello'"
    Given "  'hello'world" returns "  'hello'"
    Raises an exception if it can't tokenize a quoted string.
    :param command_str:
    :return:
    """

    pattern = re.compile(r"^((\s*)('(.*?)'))")
    mo = pattern.search(command_str)
    if mo is None:
        raise SimpleRPAException("Invalid command at index 0: a quoted string was expected")

    return mo.group(1)


def _get_parens_command_str_token(command_str):
    """
    Gets the command string token at the start of command_str. It will also be enclosed with parentheses.
    Given "(ccc)world" returns "(ccc)"
    Given "  (ccc)world" returns "  (ccc)"
    Given "(ccf10(r))world" returns "(ccf10(r))"
    Raises an exception if it can't tokenize a quoted string.
    :param command_str:
    :return:
    """

    # Check to make sure at least one open parenthesis exists:
    pattern = re.compile(r"^\s*\(")
    mo = pattern.search(command_str)
    if mo is None:
        raise SimpleRPAException("Invalid command at index 0: No open parenthesis found.")

    # Check to make sure the parentheses are balanced:
    i = 0
    open_parens_count = 0
    while i < len(command_str):
        if command_str[i] == "(":
            open_parens_count += 1
        elif command_str[i] == ")":
            open_parens_count -= 1
            if open_parens_count == 0:
                i += 1  # Remember to increment i past the ) before breaking.
                break
            elif open_parens_count == -1:
                raise SimpleRPAException("Invalid command at index 0: No open parenthesis for this close parenthesis.")
        i += 1
    if open_parens_count > 0:
        raise SimpleRPAException("Invalid command at index 0: Not enough close parentheses.")

    return command_str[0:i]


def _get_comma_token(command_str):
    """
    Gets the comma token at the start of command_str.
    Given ',' returns ','
    Given '  ,', returns '  ,'
    Raises an exception if a comma isn't found.
    :param command_str:
    :return:
    """

    pattern = re.compile(r"^((\s*),)")
    mo = pattern.search(command_str)
    if mo is None:
        raise SimpleRPAException("Invalid command at index 0: a comma was expected")

    return mo.group(1)


def _tokenize_command_str(command_str):
    """
    Tokenizes command_str into a list of commands and their arguments for the run() function. Returns the list.
    :param command_str:
    :return:
    """

    command_pattern = re.compile(r"^(su|sd|ss|c|l|m|r|g|d|k|w|h|f|s|a|p)")

    # Tokenize the command string.
    command_list = []
    i = 0  # Points to the current index in command_str that is being tokenized.

    while i < len(command_str):
        if command_str[i] in (" ", "\t", "\n", "\r"):
            # Skip over whitespace:
            i += 1
            continue

        mo = command_pattern.match(command_str[i:])
        if mo is None:
            raise SimpleRPAException("Invalid command at index %s: %s is not a valid command" % (i, command_str[i]))

        individual_command = mo.group(1)
        command_list.append(individual_command)
        i += len(individual_command)

        # Handle the no argument commands (c, l, m, r, su, sd, ss):
        if individual_command in ("c", "l", "m", "r", "su", "sd", "ss"):
            pass  # This just exists so these commands are covered by one of these cases.

        # Handle the arguments of the mouse (g)o and mouse (d)rag commands:
        elif individual_command in ("g", "d"):
            try:
                x = _get_number_token(command_str[i:])
                i += len(x)  # Increment past the x number.

                comma = _get_comma_token(command_str[i:])
                i += len(comma)  # Increment past the comma (and any whitespace).

                y = _get_number_token(command_str[i:])
                i += len(y)  # Increment past the y number.

            except SimpleRPAException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                index_part, colon, message = str(excObj).partition(":")

                index_num = index_part[len("Invalid command at index "):]
                new_index_num = int(index_num) + i
                raise SimpleRPAException("Invalid command at index %s:%s" % (new_index_num, message))

            # Make sure either both x and y have +/- or neither of them do:
            if x.lstrip()[0].isdecimal() and not y.lstrip()[0].isdecimal():
                raise SimpleRPAException("Invalid command at index %s: Y has a +/- but X does not." % (i - len(y)))
            if not x.lstrip()[0].isdecimal() and y.lstrip()[0].isdecimal():
                raise SimpleRPAException(
                    "Invalid command at index %s: Y does not have a +/- but X does." % (i - len(y))
                )

            # Get rid of any whitespace at the front:
            command_list.append(x.lstrip())
            command_list.append(y.lstrip())

        # Handle the arguments of the (s)leep and (p)ause commands:
        elif individual_command in ("s", "p"):
            try:
                num = _get_number_token(command_str[i:])
                i += len(num)  # Increment past the number.

                # TODO - raise an exception if a + or - is in the number.

            except SimpleRPAException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                index_part, colon, message = str(excObj).partition(":")

                index_num = index_part[len("Invalid command at index "):]
                new_index_num = int(index_num) + i
                raise SimpleRPAException("Invalid command at index %s:%s" % (new_index_num, message))

            # Get rid of any whitespace at the front:
            command_list.append(num.lstrip())

        # Handle the arguments of the (k)ey press, (w)rite, (h)otkeys, and (a)lert commands:
        elif individual_command in ("k", "w", "h", "a"):
            try:
                quoted_string = _get_quoted_string_token(command_str[i:])
                i += len(quoted_string)  # Increment past the quoted string.
            except SimpleRPAException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                index_part, colon, message = str(excObj).partition(":")

                index_num = index_part[len("Invalid command at index "):]
                new_index_num = int(index_num) + i
                raise SimpleRPAException("Invalid command at index %s:%s" % (new_index_num, message))

            # Get rid of any whitespace at the front and the quotes:
            command_list.append(quoted_string[1:-1].lstrip())

        # Handle the arguments of the (f)or loop command:
        elif individual_command == "f":
            try:
                number_of_loops = _get_number_token(command_str[i:])
                i += len(number_of_loops)  # Increment past the number of loops.

                subcommand_str = _get_parens_command_str_token(command_str[i:])
                i += len(subcommand_str)  # Increment past the sub-command string.

            except SimpleRPAException as excObj:
                # Exception message starts with something like "Invalid command at index 0:"
                # Change the index number and reraise it.
                index_part, colon, message = str(excObj).partition(":")

                index_num = index_part[len("Invalid command at index "):]
                new_index_num = int(index_num) + i
                raise SimpleRPAException("Invalid command at index %s:%s" % (new_index_num, message))

            # Get rid of any whitespace at the front:
            command_list.append(number_of_loops.lstrip())

            # Get rid of any whitespace at the front and the quotes:
            subcommand_str = subcommand_str.lstrip()[1:-1]
            # Recursively call this function and append the list it returns:
            command_list.append(_tokenize_command_str(subcommand_str))

    return command_list


def _run_command_list(command_list, _ss_count):
    """
    :param command_list:
    :param _ss_count:
    :return:
    """

    global PAUSE
    i = 0
    while i < len(command_list):
        command = command_list[i]

        if command == "c":
            click(button=PRIMARY)
        elif command == "l":
            click(button=LEFT)
        elif command == "m":
            click(button=MIDDLE)
        elif command == "r":
            click(button=RIGHT)
        elif command == "su":
            scroll(1)  # scroll up
        elif command == "sd":
            scroll(-1)  # scroll down
        elif command == "ss":
            screenshot("screenshot%s.png" % (_ss_count[0]))
            _ss_count[0] += 1
        elif command == "s":
            time.sleep(float(command_list[i + 1]))
            i += 1
        elif command == "p":
            PAUSE = float(command_list[i + 1])
            i += 1
        # elif command == "g":
        #    if command_list[i + 1][0] in ("+", "-") and command_list[i + 2][0] in ("+", "-"):
        #         move(int(command_list[i + 1]), int(command_list[i + 2]))
        #    else:
        #        moveTo(int(command_list[i + 1]), int(command_list[i + 2]))
        #    i += 2
        # elif command == "d":
        #    if command_list[i + 1][0] in ("+", "-") and command_list[i + 2][0] in ("+", "-"):
        #        drag(int(command_list[i + 1]), int(command_list[i + 2]))
        #    else:
        #        dragTo(int(command_list[i + 1]), int(command_list[i + 2]))
        #    i += 2
        elif command == "k":
            press(command_list[i + 1])
            i += 1
        elif command == "w":
            type(command_list[i + 1])
            i += 1
        # elif command == "h":
        #    hotkey(*command_list[i + 1].replace(" ", "").split(","))
        #    i += 1
        # elif command == "a":
        #    alert(command_list[i + 1])
        #    i += 1
        elif command == "f":
            for j in range(int(command_list[i + 1])):
                _run_command_list(command_list[i + 2], _ss_count)
            i += 2
        i += 1
# endregion


class test:
    app = None

    def __iter__(self):
        """Raise to avoid infinite loops"""
        raise NotImplementedError("Object is not iterable, try to use .windows()")

    def __getitem__(self, index):
        return self.app[index]

    def __getattribute__(self, attr_name):
        return object.__getattribute__(self, attr_name)

    def start(self, path):
        self.app = gui.Application().start(path)


# Add the bottom left, top right, and bottom right corners to FAILSAFE_POINTS.
_right, _bottom = size()
FAILSAFE_POINTS.extend([(0, _bottom - 1), (_right - 1, 0), (_right - 1, _bottom - 1)])
