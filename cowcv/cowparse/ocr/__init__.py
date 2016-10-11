#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ocr
-----------

:copyright: 2016-09-29 by hbldh <henrik.blidh@nedomkull.com>

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import cv2
from PIL import Image

from cowcv.cowparse.ocr.classify import classify
from cowcv.cowparse.geometry.bbox import BoundingBox


def detect_digits_in_roi(cowface, roi_bb):
    cowface_gray = cv2.cvtColor(cowface[:, :, ::-1], cv2.COLOR_BGR2GRAY)
    roi, roi_map = roi_bb(cowface), roi_bb.active_region
    roi_gray = cv2.cvtColor(roi[:, :, ::-1], cv2.COLOR_BGR2GRAY)

    mser = cv2.MSER_create()
    regions = mser.detectRegions(roi_gray, None)
    mser_bbs = [BoundingBox.create_from_coordinates(
        r, relative_to=roi_bb) for r in regions]

    digits = []
    for possible_digit_region in mser_bbs:

        # First simple filtering
        if possible_digit_region.aspect_ratio < 3.0:
            continue
        if possible_digit_region.active_region_solidity < 0.3:
            continue

        digit = classify(possible_digit_region(cowface_gray),
                         possible_digit_region)
        if digit is not None:
            digits.append((digit, possible_digit_region))

    i = cowface.copy()
    for d in digits:
        d[1].draw_box(i)
    Image.fromarray(i).show()

    return digits


