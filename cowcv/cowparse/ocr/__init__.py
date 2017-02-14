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

    mser = cv2.MSER_create(_min_area=50*50, _min_diversity=50.0)
    regions = mser.detectRegions(roi_gray, None)
    mser_bbs = [BoundingBox.create_from_coordinates(
        r, relative_to=roi_bb) for r in regions]

    digits = []
    for possible_digit_region in mser_bbs:

        # First, simple filtering on geometric properties.
        if possible_digit_region.aspect_ratio > 3.0:
            continue
        if possible_digit_region.active_region_solidity < 0.3:
            continue

        digit = classify(possible_digit_region(cowface),
                         possible_digit_region)
        if digit is not None:
            digits.append((digit, possible_digit_region))

    i = cowface.copy()
    roi_bb.draw_box(i, [255, 0, 0])
    for d in digits:
        d[1].draw_box(i)
    Image.fromarray(i).show()

    return digits


# def detect_digits_in_roi_er(cowface, roi_bb):
#     CATFACE_DETECTOR = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalcatface_extended.xml"
#
#     roi = roi_bb(cowface)
#
#     channels = cv2.text.computeNMChannels(roi)
#     # Append negative channels to detect ER- (bright regions over dark background)
#     cn = len(channels) - 1
#     for c in range(0, cn):
#         channels.append((255 - channels[c]))
#
#     # Apply the default cascade classifier to each independent channel (could be done in parallel)
#     print("Extracting Class Specific Extremal Regions from " + str(
#         len(channels)) + " channels ...")
#     print("    (...) this may take a while (...)")
#     for channel in channels:
#         erc1 = cv2.text.loadClassifierNM1(
#             pathname + '/trained_classifierNM1.xml')
#         er1 = cv2.text.createERFilterNM1(erc1, 16, 0.00015, 0.13, 0.2, True,
#                                          0.1)
#
#         erc2 = cv2.text.loadClassifierNM2(
#             pathname + '/trained_classifierNM2.xml')
#         er2 = cv2.text.createERFilterNM2(erc2, 0.5)
#
#         regions = cv2.text.detectRegions(channel, er1, er2)
#
#         rects = cv2.text.erGrouping(img, channel, [r.tolist() for r in regions])

