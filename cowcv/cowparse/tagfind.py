#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tagfind
-----------

:copyright: 2016-09-27 by hbldh <henrik.blidh@nedomkull.com>

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np
import cv2
from PIL import Image


def find_yellow_tag_candidates(cowface):

    cowface_blob = yellow_areas(cowface)
    #Image.fromarray(cowface_blob).show()

    kernel = np.ones((3, 3), np.uint8)
    cowface_blob = cv2.dilate(cowface_blob, kernel, iterations=10)
    cowface_blob = cv2.erode(cowface_blob, kernel, iterations=11)
    #Image.fromarray(sure_bg).show()
    image, contours, hierarchy = cv2.findContours(cowface_blob, cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)

    roi_array = []
    for c in contours:
        x_min, y_min = c.min(axis=0).flatten()
        x_max, y_max = c.max(axis=0).flatten()
        roi = cowface[y_min:y_max, x_min:x_max, :].copy()
        roi_map = cowface_blob[y_min:y_max, x_min:x_max] > 0
        roi[roi_map == 0] = np.array(roi[roi_map > 0].mean(axis=0), 'uint8')
        roi_array.append((roi, roi_map))
        #Image.fromarray(roi).show()

    roi_array.sort(key=lambda x: np.prod(x[0].shape), reverse=True)

    return roi_array


def yellow_areas(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_image = cv2.inRange(hsv, (60,60,60), (110, 255, 255))
    #Image.fromarray(yellow_image).show()
    return yellow_image


