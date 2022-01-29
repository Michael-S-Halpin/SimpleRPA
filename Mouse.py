# region License
"""
 * SimplRPA - A simple RPA library for Python and C#
 *
 * Copyright (c) 2009-2021 Michael Halpin
 * Modifications (c) as per Git change history
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
import pytweening
import _Platform_Convergence
from _Widget import Widget


# Constants for the mouse button names:
class Btn:
    """
    An enumerated list of clickable mouse buttons.
    """
    LEFT = "left"
    MIDDLE = "middle"
    RIGHT = "right"
    PRIMARY = "primary"
    SECONDARY = "secondary"


# Constants for Mouse Tweening
class Tweening:
    """
    An enumerated list of all the different ways to tween the mouse.
    """
    LINEAR = pytweening.linear
    IN_QUAD = pytweening.easeInQuad
    OUT_QUAD = pytweening.easeOutQuad
    IN_OUT_QUAD = pytweening.easeInOutQuad
    IN_CUBIC = pytweening.easeInCubic
    OUT_CUBIC = pytweening.easeInOutQuad
    IN_OUT_CUBIC = pytweening.easeInOutCubic
    IN_QUART = pytweening.easeInQuart
    OUT_QUART = pytweening.easeOutQuart
    IN_OUT_QUART = pytweening.easeInOutQuart
    IN_QUINT = pytweening.easeInQuint
    OUT_QUINT = pytweening.easeOutQuint
    IN_OUT_QUINT = pytweening.easeInOutQuint
    IN_SINE = pytweening.easeInSine
    OUT_SINE = pytweening.easeOutSine
    IN_OUT_SINE = pytweening.easeInOutSine
    IN_EXPO = pytweening.easeInExpo
    OUT_EXPO = pytweening.easeOutExpo
    IN_OUT_EXPO = pytweening.easeInOutExpo
    IN_CIRC = pytweening.easeInCirc
    OUT_CIRC = pytweening.easeOutCirc
    IN_OUT_CIRC = pytweening.easeInOutCirc
    IN_ELASTIC = pytweening.easeInElastic
    OUT_ELASTIC = pytweening.easeOutElastic
    IN_OUT_ELASTIC = pytweening.easeInOutElastic
    IN_BACK = pytweening.easeInBack
    OUT_BACK = pytweening.easeOutBack
    IN_OUT_BACK = pytweening.easeInOutBack
    IN_BOUNCE = pytweening.easeInBounce
    OUT_BOUNCE = pytweening.easeOutBounce
    IN_OUT_BOUNCE = pytweening.easeInOutBounce


# noinspection GrazieInspection
class MouseConfig:
    """
    Instances contain the configuration settings for how a mouse operation should be performed.
    :prop use_widgets: If true displays the field highlighting widget during operation.
    :prop widget_duration: How long to display the widget on the screen.
    :prop log_screenshot: If true the method takes a screenshot after the action.
    :prop tween: How you would like to tween the mouse.
    :prop action_duration: The amount of time to take to perform the operation.
    :prop pause_after: How many seconds to pause after the operation ahs been performed.
    """
    use_widgets = False  #
    widget_duration = 0.0  #
    log_screenshot = False  #
    tween = Tweening.LINEAR  #
    action_duration = 0.0  #
    pause_after = 0.0  #


# METHODS
# noinspection GrazieInspection
class Mouse:
    @staticmethod
    def move(pt, config=None):
        """
        Moves the mouse to the specified point.
        :param pt: A tuple of the point on the screen.
        :param config: The configuration object that contains setting for how this action should be performed.
        :return: void
        """

        if config is None:
            config = MouseConfig()

        if config.use_widgets:
            if pt is None:
                pt = Mouse.position()
            Widget.show_widget_pt(pt, config.widget_duration)

        _Platform_Convergence.move_to(pt[0], pt[1], config.action_duration, config.tween, config.log_screenshot,
                                      config.pause_after)

    @staticmethod
    def click(pt=None, clicks=1, interval=0.0, button=Btn.PRIMARY, config=None):
        """
        Move to the point (if specified) and clicks the specified mouse button.
        :param pt: Tuple point on the screen to click on.
        :param clicks: The number of clicks to perform.
        :param interval: The time to take between clicks.
        :param button: Which button to click with.
        :param config: The configuration object that contains setting for how this action should be performed.
        :return: void
        """

        x, y, config = Mouse._validate_point(pt, config)
        _Platform_Convergence.click(x, y, clicks, interval, button, config.action_duration, config.tween,
                                    config.log_screenshot, config.pause_after)

    @staticmethod
    def down(pt=None, button=Btn.PRIMARY, config=None):
        """
        Move to the point (if specified) and presses the specified mouse button down.
        :param pt: Tuple point on the screen to click on.
        :param button: Which button to click with.
        :param config: The configuration object that contains setting for how this action should be performed.
        :return: void
        """

        x, y, config = Mouse._validate_point(pt, config)
        _Platform_Convergence.mouse_down(x, y, button, config.tween, config.log_screenshot, config.pause_after)

    @staticmethod
    def up(pt=None, button=Btn.PRIMARY, config=None):
        """
        Move to the point (if specified) and releases the specified mouse button.
        :param pt: Tuple point on the screen to move to.
        :param button: Which button to click with.
        :param config: The configuration object that contains setting for how this action should be performed.
        :return: void
        """

        x, y, config = Mouse._validate_point(pt, config)
        _Platform_Convergence.mouse_up(x, y, button, config.tween, config.log_screenshot, config.pause_after)

    @staticmethod
    def scroll(clicks=1, pt=None, config=None):
        """
        Clicks the scroll wheel on the mouse. Positive number scrolls up, negative number scrolls down.
        :param clicks: The number of clicks to make.
        :param pt: The point on the screen to move to.
        :param config: The configuration object that contains setting for how this action should be performed.
        :return: void
        """

        x = None
        y = None

        if isinstance(pt, type((int, int))):
            x = pt[0]
            y = pt[1]

        elif not isinstance(pt, type(None)):
            raise NotImplementedError('Type of pt must be tuple or none.')

        if config is None:
            config = MouseConfig()

        _Platform_Convergence.scroll(clicks, x, y, config.log_screenshot, config.pause_after)
        print()

    @staticmethod
    def drag(start_pt, end_pt, button=Btn.PRIMARY, config=None):
        """
        Moves to the start point, clicks and drags to the end point and releases the mouse.
        :param start_pt: The point to move to before clicking.
        :param end_pt: The point to drag to after clicking.
        :param button: Which button to click with.
        :param config: The configuration object that contains setting for how this action should be performed.
        :return: void
        """

        if config is None:
            config = MouseConfig()

        if config.use_widgets:
            if start_pt is None:
                start_pt = Mouse.position()

            if end_pt is None:
                end_pt = Mouse.position()

            Widget.show_widget_pt(start_pt, config.duration / 2)
            Widget.show_widget_pt(end_pt, config.duration)

        _Platform_Convergence.mouse_move_drag('drag', start_pt[0], start_pt[1], end_pt[0], end_pt[1],
                                              config.action_duration, config.tween, button, config.log_screenshot)

    @staticmethod
    def position():
        """
        Gets a tuple coordinate of where the mouse is located at.
        :return: tuple
        """
        return _Platform_Convergence.position()

    @staticmethod
    def _validate_point(pt, config):

        x = None
        y = None

        if isinstance(pt, type((int, int))):
            x = pt[0]
            y = pt[1]

        elif not isinstance(pt, type(None)):
            raise NotImplementedError('Type of pt must be tuple of none.')

        if config is None:
            config = MouseConfig()

        if config.use_widgets:
            if pt is None:
                pt = Mouse.position()

            Widget.show_widget_pt(pt, config.duration)

        return x, y, config
