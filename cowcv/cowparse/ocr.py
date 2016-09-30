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


def detect_digits_in_roi(roi_spec):
    roi, roi_map = roi_spec
    Image.fromarray(roi).show()

    roi_gray = cv2.cvtColor(roi[:, :, ::-1], cv2.COLOR_BGR2GRAY)
    #roi_gray[-roi_map] = 255

    h = np.histogram(roi_gray[roi_map], bins=256)

    th2 = cv2.adaptiveThreshold(roi_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                cv2.THRESH_BINARY, 20, 1)
    th3 = cv2.adaptiveThreshold(roi_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                cv2.THRESH_BINARY, 20, 1)
    Image.fromarray(th2).show()
    Image.fromarray(th3).show()

    #blurred = cv2.GaussianBlur(roi_gray, (5, 5), 0)
    #pixels = blurred[roi_map].flatten()
    #ret, cowface_blob = cv2.threshold(pixels, 0, 255,
    #                                  cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    roi_gray[roi_gray < ret] = 0
    roi_gray[roi_gray >= ret] = 255

    Image.fromarray(roi_gray).show()

    return []

