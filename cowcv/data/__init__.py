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

_COW_URLS = {
    1: "https://dl.dropboxusercontent.com/u/21298554/cow1.jpg",
    2: "https://dl.dropboxusercontent.com/u/21298554/cow2.jpg",
    3: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Kossa-2.jpg/800px-Kossa-2.jpg",
    4: "http://obj.imagedesk.se/obj/photo/3c/3cf3d13b57dd0a5d1a93cad63681c995.jpg",
    5: "http://www.opps.se/roliga-kor-i-askloster-ko-bilder-168-ab.jpg",
    6: "http://cdn.lovelylife.se/blogs/4/2015/12/Kor_LR.jpg",
    7: "http://www.zolaenterprises.com/P1200084cs.jpg",
    8: "http://www.opps.se/P1300244roliga-kor.jpg"
}
_COW_FACE_COORDS = {
    1: (900, 500, 2650 - 900, 2150 - 800),
    2: (450, 700, 3350 - 450, 3000 - 700),
    3: None,
    4: None
}

def get_cow(nbr=1):
    image_path = pathlib.Path(
        __file__).resolve().parent.joinpath('cow{0}.jpg'.format(nbr))
    if image_path.exists():
        return Image.open(str(image_path))
    else:
        r = urlopen(_COW_URLS.get(nbr))
        with open(str(image_path), 'wb') as f:
            f.write(r.read())
        return get_cow(nbr)

def get_cow_face_coordinates(nbr=1):
    return _COW_FACE_COORDS.get(nbr)


def _image(pth, url):
    """Load image specified in ``path``. If not present,
    fetch it from ``url`` and store locally.

    :param str or :class:`~pathlib.Path` pth:
    :param str url: URL from where to fetch the image.
    :return: The :class:`~PIL.Image` requested.

    """

