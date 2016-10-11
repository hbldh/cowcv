#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bbox
-----------

:copyright: 2016-10-11 by hbldh <henrik.blidh@nedomkull.com>

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import numpy as np
from cowcv.cowparse.geometry.polygon import Polygon


class BoundingBox(Polygon):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        super(BoundingBox, self).__init__(np.squeeze(self.contour, axis=1))
        self.active_region = None

    def __str__(self):
        return "BoundingBox: [{0}:{1}, {2}:{3}]".format(
            self.y, self.y + self.h, self.x, self.x + self.w)

    def __repr__(self):
        return str(self)

    def __call__(self, *args, **kwargs):
        return self.extract(args[0])

    @property
    def shape(self):
        return self.h, self.w

    @property
    def aspect_ratio(self):
        return self.w / self.h

    @property
    def active_region_solidity(self):
        if self.active_region is not None:
            return self.active_region.sum() / self.area
        else:
            return 0.0

    @property
    def contour(self):
        return np.array([
            [[self.y, self.x], ],
            [[self.y, self.x + self.w], ],
            [[self.y + self.h, self.x + self.w], ],
            [[self.y + self.h, self.x], ],
        ])

    def extract(self, img):
        if img.ndim == 3:
            out = img[self.y:self.y + self.h, self.x:self.x + self.w, :]
        else:
            out = img[self.y:self.y + self.h, self.x:self.x + self.w]
        np.testing.assert_almost_equal(out.shape[:2], self.shape)
        return out

    def add_active_region(self, region):
        if region.shape[:2] != (self.h, self.w):
            raise ValueError()
        else:
            self.active_region = region

    @classmethod
    def create_from_coordinates(cls, c, relative_to=None):
        x_min, y_min = c.min(axis=0).flatten()
        x_max, y_max = c.max(axis=0).flatten()
        x, y, w, h = x_min, y_min, x_max - x_min + 1, y_max - y_min + 1

        out = cls(x, y, w, h)

        active_region = np.zeros(out.shape, dtype='bool')
        if c.ndim == 3:
            c = np.squeeze(c, axis=1)
        for p in c - [out.x, out.y]:
            active_region[p[1], p[0]] = True
        out.add_active_region(active_region)

        if relative_to is not None:
            if isinstance(relative_to, cls):
                out.x += relative_to.x
                out.y += relative_to.y
            else:
                out.x += relative_to[0]
                out.y += relative_to[1]

        return out

    def draw_box(self, img, color=(0, 255, 0)):
        img[self.y, self.x:self.x + self.w] = color
        img[self.y:self.y + self.h, self.x + self.w] = color
        img[self.y + self.h, self.x:self.x + self.w] = color
        img[self.y: self.y + self.h, self.x] = color
        return img

    def fill_active_region(self, img, color=(255, 0, 0)):
        self.extract(img)[self.active_region] = color
        return img
