#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
facefind
-----------

:copyright: 2016-09-27 by hbldh <henrik.blidh@nedomkull.com>

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import cv2

def find_cowface(img):
    return 0, 0, img.size[0], img.size[1]
