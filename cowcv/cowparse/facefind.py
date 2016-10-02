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
import numpy as np
from PIL import Image, ImageDraw
from cowcv.cowparse.utils import BoundingBox




def find_cowface(image):
    #CATFACE_DETECTOR = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalcatface_extended.xml"
    #detector = cv2.CascadeClassifier(CATFACE_DETECTOR)
    # img = np.array(image)[:, :, ::-1]
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #
    # # load the cat detector Haar cascade, then detect cat faces
    # # in the input image
    # rects = detector.detectMultiScale(gray, scaleFactor=1.1,
    #                                   minNeighbors=2, minSize=(75, 75))
    #
    # imgcopy = img[:, :, ::-1]
    # # loop over the cat faces and draw a rectangle surrounding each
    # for (i, (x, y, w, h)) in enumerate(rects):
    #
    #     imgcopy[y, x:x+w] = [0, 255, 0]
    #     imgcopy[y:y+h, x + w] = [0, 255, 0]
    #     imgcopy[y + h, x:x+w] = [0, 255, 0]
    #     imgcopy[y: y + h, x] = [0, 255, 0]
    #
    # Image.fromarray(imgcopy).show()
    #
    # # show the detected cat faces
    # cv2.imshow("Cat Faces", img)
    #
    # cowfaces = []
    # for r in rects:
    #     cowfaces.append(BoundingBox(*r))
    # cowfaces.sort(key=lambda x: np.prod(x.shape), reverse=True)
    #
    # return cowfaces[0]
    return BoundingBox(0, 0, image.size[0], image.size[1])
