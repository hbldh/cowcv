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
from PIL import Image

from cowcv.data import cow2, cow2, cow1_face_coordinates, cow2_face_coordinates
from cowcv.cowparse import facefind, tagfind, ocr, utils

cow2 = cow2()
cowface2_bb = utils.BoundingBox(*cow2_face_coordinates())
cowface = cowface2_bb(np.array(cow2))

rois = tagfind.find_yellow_tag_candidates(cowface)

for roi in rois[1:]:
    digits = ocr.detect_digits_in_roi(cowface, roi)
    print(digits)



