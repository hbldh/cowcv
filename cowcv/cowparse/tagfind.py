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


def find_yellow_tag_tutorial(cowface):
    normed_yellow_img = np.linalg.norm((np.array(
        cowface[:, :, :2], 'float')) / 2, axis=2)
    cowface_RG = np.array((normed_yellow_img /
                        normed_yellow_img.max()) * 255.0, 'uint8')
    ret, cowface_blob = cv2.threshold(cv2.GaussianBlur(cowface_RG, (5, 5), 0),
                                      0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(cowface_blob, cv2.MORPH_OPEN, kernel, iterations=2)

    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Finding sure foreground area
    #dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    #ret, sure_fg = cv2.threshold(dist_transform, 0.95 * dist_transform.max(),
    #                             255, 0)

    # Finding unknown region
    #sure_fg = np.uint8(sure_fg)
    #unknown = cv2.subtract(sure_bg, sure_fg)

    Image.fromarray(sure_bg).show()
    #Image.fromarray(sure_fg).show()
    #Image.fromarray(unknown).show()

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_bg)

    # Add one to all labels so that sure background is not 0, but 1
    #markers = markers + 1

    # Now, mark the region of unknown with zero
    #markers[unknown == 255] = 0

    markers = cv2.watershed(cowface, markers)
    cowface[markers == -1] = [255, 0, 0]

    Image.fromarray(cowface).show()

    #return thresholded_cowface


def find_yellow_tag_candidates(cowface):
    normed_yellow_img = np.linalg.norm((np.array(
        cowface[:, :, :2], 'float')) / 2, axis=2)
    cowface_RG = np.array((normed_yellow_img /
                        normed_yellow_img.max()) * 255.0, 'uint8')
    ret, cowface_blob = cv2.threshold(cv2.GaussianBlur(cowface_RG, (5, 5), 0),
                                      0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(cowface_blob, cv2.MORPH_OPEN, kernel, iterations=5)
    sure_bg = cv2.dilate(opening, kernel, iterations=10)

    image, contours, hierarchy = cv2.findContours(sure_bg, cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)
    cowface_roi = cowface.copy()
    cowface_roi[sure_bg == 0] = [0, 0, 0]
    #cowface_roi = cowface_RG.copy()
    #cowface_roi[sure_bg == 0] = 255

    roi_array = []
    for c in contours:
        x_min, y_min = c.min(axis=0).flatten()
        x_max, y_max = c.max(axis=0).flatten()
        roi = cowface_roi[y_min:y_max, x_min:x_max, :]
        roi_map = sure_bg[y_min:y_max, x_min:x_max] > 0
        roi_array.append((roi, roi_map))

    roi_array.sort(key=lambda x: np.prod(x[0].shape))

    return roi_array
