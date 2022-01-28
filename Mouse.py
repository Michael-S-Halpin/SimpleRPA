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
    LINEAR = _Platform_Convergence.linear
    IN_QUAD = _Platform_Convergence.easeInQuad
    OUT_QUAD = _Platform_Convergence.easeOutQuad
    IN_OUT_QUAD = _Platform_Convergence.easeInOutQuad
    IN_CUBIC = _Platform_Convergence.easeInCubic
    OUT_CUBIC = _Platform_Convergence.easeInOutQuad
    IN_OUT_CUBIC = _Platform_Convergence.easeInOutCubic
    IN_QUART = _Platform_Convergence.easeInQuart
    OUT_QUART = _Platform_Convergence.easeOutQuart
    IN_OUT_QUART = _Platform_Convergence.easeInOutQuart
    IN_QUINT = _Platform_Convergence.easeInQuint
    OUT_QUINT = _Platform_Convergence.easeOutQuint
    IN_OUT_QUINT = _Platform_Convergence.easeInOutQuint
    IN_SINE = _Platform_Convergence.easeInSine
    OUT_SINE = _Platform_Convergence.easeOutSine
    IN_OUT_SINE = _Platform_Convergence.easeInOutSine
    IN_EXPO = _Platform_Convergence.easeInExpo
    OUT_EXPO = _Platform_Convergence.easeOutExpo
    IN_OUT_EXPO = _Platform_Convergence.easeInOutExpo
    IN_CIRC = _Platform_Convergence.easeInCirc
    OUT_CIRC = _Platform_Convergence.easeOutCirc
    IN_OUT_CIRC = _Platform_Convergence.easeInOutCirc
    IN_ELASTIC = _Platform_Convergence.easeInElastic
    OUT_ELASTIC = _Platform_Convergence.easeOutElastic
    IN_OUT_ELASTIC = _Platform_Convergence.easeInOutElastic
    IN_BACK = _Platform_Convergence.easeInBack
    OUT_BACK = _Platform_Convergence.easeOutBack
    IN_OUT_BACK = _Platform_Convergence.easeInOutBack
    IN_BOUNCE = _Platform_Convergence.easeInBounce
    OUT_BOUNCE = _Platform_Convergence.easeOutBounce
    IN_OUT_BOUNCE = _Platform_Convergence.easeInOutBounce


class MouseConfig:
    """
    Instances contain the configuration settings for how a mouse operation should be performed.
    """
    use_widgets = False  # If true displays the field highlighting widget during operation.
    widget_duration = 0.0  # How long to display the widget on the screen.
    log_screenshot = False  # If true the method takes a screenshot after the action.
    tween = Tweening.LINEAR  # How you would like to tween the mouse.
    action_duration = 0.0  # The amount of time to take to perform the operation.
    pause_after = 0.0  # How many seconds to pause after the operation ahs been performed.


# METHODS
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
