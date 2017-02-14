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

from cowcv.data import get_cow, get_cow_face_coordinates
from cowcv.cowparse import facefind, tagfind, ocr

nbr = 2

cow = get_cow(nbr)
#cowface_bb = utils.BoundingBox(*get_cow_face_coordinates(nbr))
cowface_bb = facefind.find_cowface(cow)
cowface = cowface_bb(np.array(cow))

rois = tagfind.find_yellow_tag_candidates(cowface)
#rois2 = tagfind.find_yellow_tag_candidates_optional(cowface)

import cowcv.data.ocr.data
for roi in rois:
    digits = ocr.detect_digits_in_roi(cowface, roi)
    print(digits)



