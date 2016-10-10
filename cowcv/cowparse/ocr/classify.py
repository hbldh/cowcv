#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
classify
-----------

:copyright: 2016-10-10 by hbldh <henrik.blidh@nedomkull.com>

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import hashlib
import io
import pathlib
import pickle

from PIL import Image

SAVE_IMAGES = True
OCR_DATA_DIR = pathlib.Path(
    __file__).resolve().parent.parent.parent.joinpath('data', 'ocr')


def classify(img, bb):
    if SAVE_IMAGES:
        with io.BytesIO() as bio:
            Image.fromarray(img).save(bio, format='png')
            bio.seek(0)
            img_md5 = hashlib.md5(bio.read())
            bio.seek(0)

        with open(str(OCR_DATA_DIR.joinpath(str(img_md5) + '.png'))) as f:
            f.write(bio.read())
        with open(str(OCR_DATA_DIR.joinpath(str(img_md5) + '.pkl'))) as f:
            pickle.dump(f, bb)

    return None


def extract_features(img, bb):
    pass

