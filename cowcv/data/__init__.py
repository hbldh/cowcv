#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

import imdirect
imdirect.monkey_patch()
from PIL import Image

_COW1_URL = "https://dl.dropboxusercontent.com/u/21298554/cow1.jpg"
_COW2_URL = "https://dl.dropboxusercontent.com/u/21298554/cow2.jpg"
_COW3_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Kossa-2.jpg/800px-Kossa-2.jpg"


def cow1():
    """The first test cow JPEG.

    :return: The PIL image of first test cow.

    """
    image_path = pathlib.Path(
        __file__).resolve().parent.joinpath('cow1.jpg')
    return _image(image_path, _COW1_URL)


def cow1_face_coordinates():
    """
    (960, 710), (2650, 2150)

    :return:
    """
    x = 900
    y = 800
    w = 2650 - x
    h = 2150 - y

    return x, y, w, h


def cow2():
    """The second test cow JPEG.

    :return: The PIL image of second test cow.

    """
    image_path = pathlib.Path(
        __file__).resolve().parent.joinpath('cow2.jpg')
    return _image(image_path, _COW2_URL)


def cow2_face_coordinates():
    """
    (700, 450), (3350, 3000)

    :return:
    """
    y = 700
    x = 450
    w = 3350 - x
    h = 3000 - y

    return x, y, w, h


def cow3():
    """The third test cow JPEG.

    :return: The PIL image of third test cow.

    """
    image_path = pathlib.Path(
        __file__).resolve().parent.joinpath('cow3.jpg')
    return _image(image_path, _COW1_URL)


def cow3_face_coordinates():
    """

    :return:
    """
    x = 0
    y = 0
    w = 2650 - x
    h = 2150 - y

    return x, y, w, h


def _image(pth, url):
    """Load image specified in ``path``. If not present,
    fetch it from ``url`` and store locally.

    :param str or :class:`~pathlib.Path` pth:
    :param str url: URL from where to fetch the image.
    :return: The :class:`~PIL.Image` requested.

    """
    if pth.exists():
        return Image.open(str(pth))
    else:
        r = urlopen(url)
        with open(str(pth), 'wb') as f:
            f.write(r.read())
        return _image(pth, url)
