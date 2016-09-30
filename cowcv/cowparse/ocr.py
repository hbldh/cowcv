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
    roi, roi_map = roi_bb(cowface), roi_bb.active_region

    roi_gray = cv2.cvtColor(roi[:, :, ::-1], cv2.COLOR_BGR2GRAY)

    th2 = cv2.adaptiveThreshold(roi_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 51, 1)
    th3 = cv2.adaptiveThreshold(roi_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                cv2.THRESH_BINARY, 51, 1)

    blurred = cv2.GaussianBlur(roi_gray, (5, 5), 0)
    pixels = blurred[roi_map].flatten()
    ret, cowface_blob = cv2.threshold(pixels, 0, 255,
                                      cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    ut = roi_gray.copy()
    ut[roi_gray < ret] = 0
    ut[roi_gray >= ret] = 255

    #Image.fromarray(ut).show()

    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(th3, kernel, iterations=3)
    img = cv2.erode(img, kernel, iterations=2)

    mser = cv2.MSER_create()
    regions = mser.detectRegions(roi_gray, None)

    mser_bbs = []
    for r in regions:
        bb = BoundingBox.create_from_coordinates(r, relative_to=roi_bb)
        bb_non_rel = BoundingBox.create_from_coordinates(r)
        ar = np.zeros(bb.shape, 'bool')
        ar[r - [bb_non_rel.x, bb_non_rel.y]] = 1
        #for p in r:
        #    ar[p] = 1
        bb.add_active_region(ar)
        mser_bbs.append(bb)
        this_img = cv2.drawContours(cowface.copy(), [bb.contour], 0, (255, 0, 0), 3)
        Image.fromarray(this_img).show()


    return []

