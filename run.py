#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:`run`
=======================

.. moduleauthor:: hbldh <henrik.blidh@nedomkull.com>
Created on 2016-09-12, 09:44

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np

from cowcv.data import cow1, cow2, cow1_face_coordinates, cow2_face_coordinates
from cowcv.cowparse import facefind, tagfind, ocr

cow1 = cow2()
x,y,w,h = cow2_face_coordinates()
# x,y,w,h = facefind.find_cowface(cow1)
cowface = np.array(cow1)[y:y+h, x:x+w, :]

rois = tagfind.find_yellow_tag_candidates(cowface)
#rois = tagfind.find_yellow_tag_tutorial(cowface)
for roi in rois:
    digits = ocr.detect_digits_in_roi(roi)
    print(digits)



