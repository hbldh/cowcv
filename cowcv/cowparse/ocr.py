#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ocr
-----------

:copyright: 2016-09-29 by hbldh <henrik.blidh@nedomkull.com>

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np
from PIL import Image
import cv2

from cowcv.cowparse.utils import BoundingBox

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
        subimg = possible_digit_region(cowface_gray)
        mean_active_region = subimg[possible_digit_region.active_region].mean()
        mean_inactive_region = subimg[-possible_digit_region.active_region].mean()

        if np.abs(mean_active_region - mean_inactive_region) < 40:
            pass
        else:
            digit = _classify(subimg, possible_digit_region)
            if digit is not None:
                digits.append((digit, possible_digit_region))

        Image.fromarray(possible_digit_region.fill_active_region(cowface.copy())).show()

    return digits


def _classify(img, bb):
    return None
