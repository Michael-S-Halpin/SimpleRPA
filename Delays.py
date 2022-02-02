import cv2
import time
from . import _Convergence
from . import Screen


# noinspection GrazieInspection
class DelayConfig:
    """
    Instances contain the configuration settings for how a delay operation should be performed.
    :prop timeout: How long to wait for a timeout to occur.
    :prop threshold: The percentile matching threshold to determine how close a match needs to be.
    :prop log_screenshot: If true the method takes a screenshot after the action.
    """
    timeout = 30
    threshold = 1
    log_screenshot = False


def wait(seconds):
    # noinspection GrazieInspection
    """
    Waits for the specified number of seconds.
    :param seconds: The amount of time to wait in seconds.
    :return: None
    """
    time.sleep(seconds)


def wait_for_color(pt, rgb, config=None):
    # noinspection GrazieInspection
    """
    Waits for the specified color at the specified location.
    :param pt: The point on the screen to look for pixel color change.
    :param rgb: The color we are looking for.
    :param config: The configuration object that contains setting for how this action should be performed.
    :return: Boolean
    """

    response = False

    if config is None:
        config = DelayConfig()

    end = time.time() + config.timeout
    while time.time() < end:
        clr = Screen.get_pixel_color(pt)
        if config.threshold == 1:  # If match threshold is 100% do simple comparison.
            if clr == rgb:
                return True  # Return true on matching color.
        elif config.threshold > 1 or config.threshold < 0:  # Raise exception for values that are out of bounds.
            raise ValueError('The parameter "percent" may only contain percentile values between 0 and 1. (For '
                             'example .25, .66, .8, ect.)')
        else:  # If threshold is set to another value do more complicated comparison.
            r1 = rgb[0] * config.threshold
            g1 = rgb[1] * config.threshold
            b1 = rgb[2] * config.threshold
            r2 = rgb[0] * (1 - config.threshold) + 1
            g2 = rgb[1] * (1 - config.threshold) + 1
            b2 = rgb[2] * (1 - config.threshold) + 1
            if r1 < clr[0] < r2 and g1 < clr[1] < g2 and b1 < clr[2] < b2:
                response = True
                break

    # noinspection PyProtectedMember
    _Convergence._log_screenshot(config.log_screenshot, "wait_for_color", "%s,%s:%s,%s,%s" %
                                 (pt[0], pt[1], rgb[0], rgb[1], rgb[2]), folder=".")

    return response


def wait_for_image(pt, file, config=None):
    # noinspection GrazieInspection
    """
    Waits for the screen to update to something similar to the specified image at the specified point of the screen.
    :param pt: The point on the screen to look for an update at.
    :param file: The image file to use for a comparison.
    :param config: The configuration object that contains setting for how this action should be performed.
    :return: Boolean
    """

    response = False

    if file is None or file == '':
        raise FileNotFoundError("The parameter 'file' must be populated.")

    if config is None:
        config = DelayConfig()

    # Load the image file to look for.
    img = cv2.imread(file)
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    end = time.time() + config.timeout
    y = pt[1] + img1.shape[0]
    x = pt[0] + img1.shape[1]
    while time.time() < end:
        img2 = Screen.capture((pt[0], pt[1], x, y))

        # noinspection PyProtectedMember
        threshold = Screen._compare_image(img1, img2)

        if config.threshold <= threshold:
            response = True
            break

    # noinspection PyProtectedMember
    _Convergence._log_screenshot(config.log_screenshot, "wait_for_image", "%s,%s" % pt, folder=".")

    return response


def wait_for_change(rct, config=None):
    # noinspection GrazieInspection
    """
    Watches an area of the screen and waits for something to change.
    :param rct: The rectangular area of the screen to watch.
    :param config: The configuration object that contains setting for how this action should be performed.
    :return: Boolean
    """

    response = False

    if config is None:
        config = DelayConfig()

    img1 = Screen.capture(rct)

    end = time.time() + config.timeout
    while time.time() < end:
        img2 = Screen.capture(rct)
        # noinspection PyProtectedMember
        threshold = Screen._compare_image(img1, img2)
        if threshold != 1:
            response = True
            break

    # noinspection PyProtectedMember
    _Convergence._log_screenshot(config.log_screenshot, "wait_for_change", "%s,%s,%s,%s" % rct, folder=".")

    return response
