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

from cowcv.data.ocr import save_roi

SAVE_IMAGES = True


def classify(img, bb):
    if SAVE_IMAGES:
        save_roi(img, bb)

    return None


def extract_features(img, bb):
    pass

