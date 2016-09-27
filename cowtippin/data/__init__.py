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


def cow1():
    """The first test cow JPEG.

    :return: The PIL image of first test cow.

    """
    image_path = pathlib.Path(
        __file__).resolve().parent.joinpath('cow1.jpg')
    return _image(image_path, _COW1_URL)


def cow2():
    """The second test cow JPEG.

    :return: The PIL image of second test cow.

    """
    image_path = pathlib.Path(
        __file__).resolve().parent.joinpath('cow2.jpg')
    return _image(image_path, _COW1_URL)


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
