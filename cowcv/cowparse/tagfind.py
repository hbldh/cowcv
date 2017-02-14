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

from cowcv.cowparse.geometry.bbox import BoundingBox


def find_yellow_tag_candidates(cowface, limit=20):

    cowface_blob = yellow_areas(cowface)

    kernel = np.ones((3, 3), np.uint8)
    cowface_blob = cv2.dilate(cowface_blob, kernel, iterations=10)
    cowface_blob = cv2.erode(cowface_blob, kernel, iterations=11)
    image, contours, hierarchy = cv2.findContours(cowface_blob, cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)

    roi_array = []
    for c in contours:
        bb = BoundingBox.create_from_coordinates(c)
        bb.add_active_region(bb(cowface_blob) > 0)
        roi_array.append(bb)

    roi_array.sort(key=lambda x: np.prod(x.shape), reverse=True)

    #c = cowface.copy()
    #for r in roi_array:
    #    c = r.draw_box(c)
    #Image.fromarray(c).show()

    return roi_array[:limit]


def yellow_areas(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_image = cv2.inRange(hsv, (80,100,100), (110, 255, 255))
    #Image.fromarray(yellow_image).show()
    return yellow_image
