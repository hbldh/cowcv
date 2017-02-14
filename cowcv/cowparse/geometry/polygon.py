#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
polygon
-----------

:copyright: 2016-10-11 by hbldh <henrik.blidh@nedomkull.com>

"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import

import warnings

import numpy as np


class Polygon(object):
    """A class for representing polygons."""

    def __init__(self, points):
        """Constructor for Polygon"""
        self.polygon_points = np.array(points, 'float')
        if self.polygon_points.shape[1] != 2:
            raise ValueError("Polygon must be entered as a [n x 2] "
                             "array, i.e. a 2D polygon.")

    def __str__(self):
        return "Polygon with {0} vertices:\n{1}".format(
            self.polygon_points.shape[0], self.polygon_points)

    def __repr__(self):
        return str(self)

    @property
    def is_closed(self):
        """Check polygon closure.

        :return: True if the polygon is closed. False otherwise.

        """
        return np.linalg.norm(self.polygon_points[0, :] -
                              self.polygon_points[-1, :]) < 1e-10

    @property
    def closed_polygon(self):
        """Returns the closed polygon.

        Appends the first point to the end of point array,
        in order to "close" the polygon.

        """
        if not self.is_closed:
            return np.concatenate(
                [self.polygon_points, [self.polygon_points[0, :]]])
        else:
            return self.polygon_points

    @property
    def open_polygon(self):
        """Returns the open polygon.

        Removes the last point if it is close enough to the
        first, in order to "open" the polygon.

        """
        if self.is_closed:
            return self.polygon_points[:-1, :]
        else:
            return self.polygon_points

    @property
    def area(self):
        """Returns the area covered by the Polygon.

        :return: The area of the polygon.
        :rtype: float

        """
        # Abs to handle counter-clockwise ordering.
        return np.abs(self._area_help_function())

    @property
    def is_clockwise_ordered(self):
        """Property for checking if the polygon points are ordered clockwise.

        :return: Clockwise ordering status.
        :rtype: bool

        """
        return self._area_help_function() > 0

    @property
    def is_counter_clockwise_ordered(self):
        """Property for checking if the polygon points are ordered
        counter-clockwise.

        :return: Counter-clockwise ordering status.
        :rtype: bool

        """
        return self._area_help_function() < 0

    def get_center_point(self, use_centroid=True):
        """Returns a center of weight for the object.

        :param use_centroid: Uses a centroid finding method instead
            of pure mean of vertices.
        :type use_centroid: bool

        """
        if use_centroid:
            with warnings.catch_warnings(record=False) as w:
                # Cause all warnings to never be triggered.
                warnings.simplefilter("ignore")

                pnt_array = self.closed_polygon

                A = self._area_help_function()
                D = (pnt_array[:-1, 0] * pnt_array[1:, 1] -
                     pnt_array[1:, 0] * pnt_array[:-1, 1])

                c_x = ((pnt_array[:-1, 0] + pnt_array[1:, 0]) * D).sum() / (6 * A)
                c_y = ((pnt_array[:-1, 1] + pnt_array[1:, 1]) * D).sum() / (6 * A)

                if np.isnan(c_x) or np.isinf(c_x) or np.isnan(c_y) or np.isinf(c_y):
                    # If centroid calculations fails (e.g. due to zero-valued area) then use the
                    # mean of the vertices as center point instead.
                    return np.mean(self.open_polygon(), 0)
                else:
                    return np.array([c_x, c_y])
        else:
            return np.mean(self.open_polygon(), 0)

    def get_bounding_box(self):
        """Get a four point Polygon describing the bounding box of the current Polygon.

        :return: A new polygon, describing this one's bounding box.
        :rtype: :py:class:`b2ac.geometry.polygon.B2ACPolygon`

        """
        mins = self.polygon_points.min(axis=0)
        maxs = self.polygon_points.max(axis=0)
        bb_pnts = np.zeros((4, 2), dtype=self.polygon_points.dtype)
        bb_pnts[0, :] = mins
        bb_pnts[1, :] = [mins[0], maxs[1]]
        bb_pnts[2, :] = maxs
        bb_pnts[3, :] = [maxs[0], mins[1]]
        out = Polygon(bb_pnts)
        return out

    def _area_help_function(self):
        """Performing the actual area calculation.

        :return: The area of the polygon, negative if counter-clockwise
            orientation of polygon points.
        :rtype: float

        """
        # If the polygon is not closed, append first point to the end of polygon to ensure that.
        pnt_array = self.closed_polygon

        return (pnt_array[:-1, 0] * pnt_array[1:, 1] -
                pnt_array[1:, 0] * pnt_array[:-1, 1]).sum() / 2

    def overlap(self, p):
        """Get ratio of how much of ``self`` that is contained in ``p2``.

        .. note::

            Can only handle convex polygons since it uses Sutherland-Hodgman algorithm!

        Method reference:
        `Sutherland-Hodgman <http://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm>`_

        :param p1: The first polygon.
        :type p1: :py:class:`b2ac.geometry.polygon.B2ACPolygon`
        :param p2: The second polygon
        :type p2: :py:class:`b2ac.geometry.polygon.B2ACPolygon`
        :return: Value in [0, 1] describing how much of ``p1``
         that is contained in ``p2``.
        :rtype: float

        """
        # First, check if the polygons are equal. If they are, the
        # intersection calculation might encounter divide-by-zero
        # errors and is furthermore unnecessary to run...
        if np.allclose(self.polygon_points.shape, p.polygon_points.shape) and \
                np.allclose(self.polygon_points, p.polygon_points):
            return 1.0

        # Return the ratio of size of the intersection
        # and size of the subject polygon.
        intersection_polygon = self.intersection(p)
        if intersection_polygon is None:
            return 0.
        else:
            return intersection_polygon.area() / p.area()

    def intersection(self, p):
        """Returns the polygon representing the intersection of two other.

        .. note::

            Can only handle convex polygons since it uses Sutherland-Hodgman algorithm!

        Method reference:
        `Sutherland-Hodgman <http://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm>`_

        :param self: The first polygon.
        :type self: :py:class:`b2ac.geometry.polygon.B2ACPolygon`
        :param p: The second polygon
        :type p: :py:class:`b2ac.geometry.polygon.B2ACPolygon`
        :return: The intersection polygon or None if no intersection exists.
        :rtype: :py:class:`b2ac.geometry.polygon.B2ACPolygon` or :py:class:`None`.

        """
        # First remove the "closing points" of the polygon if such a vertex is present.
        p1_pnts = self.get_open_polygon()
        p2_pnts = p.get_open_polygon()

        # Perform clipping of polygons and create a new polygon instance from that.
        # TODO: Write function for ordering points clockwise in standard Cartesian plane.
        clipped_polygon_points = sutherland_hodgman_polygon_clipping(p1_pnts, p2_pnts)
        if clipped_polygon_points is not None and len(clipped_polygon_points):
            return self.__class__(clipped_polygon_points)
        else:
            return None

    def union(self, p, use_graham_scan=False):
        """Calculates the union of two polygons and returns this union polygon.

        Implementation proposals:

        1. `Polygon union <http://stackoverflow.com/questions/6844462/polygon-union-without-holes>`_
        2. Find all intersection points (Sutherland-Hodgman) to get a point cloud and
           then run the `Graham scan <http://en.wikipedia.org/wiki/Graham_scan>`_ algorithm
           on that set of points.

        :param self: The first polygon.
        :type self: :py:class:`b2ac.geometry.polygon.B2ACPolygon`
        :param p: The second polygon
        :type p: :py:class:`b2ac.geometry.polygon.B2ACPolygon`
        :param use_graham_scan: Boolean that can be used for selecting the
            slower Graham Scan convex hull algorithm instead of Quickhull.
        :type use_graham_scan: bool
        :return: The union polygon or :py:class:`None` if the polygons are not connected.
        :rtype: :py:class:`b2ac.geometry.polygon.B2ACPolygon` or :py:class:`None`

        """
        p_intersection = self.intersection(self, p)
        if p_intersection is None:
            return None
        points = np.concatenate((self.polygon_points,
                                 p.polygon_points,
                                 p_intersection.polygon_points))
        if use_graham_scan:
            return self.__class__(graham_scan(points))
        else:
            return self.__class__(quickhull(points))


def graham_scan(points):
        """Calculates the convex hull of an arbitrary 2D point cloud.

        Method reference:
        `Graham scan <http://en.wikipedia.org/wiki/Graham_scan>`_

        Code adapted from:
        `Google Code <https://mycodeplayground.googlecode.com/files/graham_scan.py>`_

        :param points: A [n x 2] array of points from which to
            estimate the convex hull.
        :type points: :py:class:`numpy.ndarray`
        :return: A [m x 2] array defining the convex hull polygon
            of the points sent in.
        :rtype: :py:class:`numpy.ndarray`

        """
        def cmp(a, b):
            return ((a > b) - (a < b))

        def angle_cmp(pivot):
            """Receive a coordinate as the pivot and return a
            function for comparing angles formed by another
            two coordinates around the pivot.
            """
            def _angle_cmp(c1, c2):
                v1 = c1[0] - pivot[0], c1[1] - pivot[1]
                v2 = c2[0] - pivot[0], c2[1] - pivot[1]
                cp = np.cross(v1, v2)
                if cp < 0:
                    return 1
                elif cp == 0:
                    return 0
                else:
                    return -1
            return _angle_cmp

        def turning(c1, c2, c3):
            """Determine which way does c1 -> c2 -> c3 turns."""
            v1 = c2[0] - c1[0], c2[1] - c1[1]
            v2 = c3[0] - c2[0], c3[1] - c2[1]
            cp = np.cross(v1, v2)
            if cp < 0:
                return 'RIGHT'
            elif cp == 0:
                return 'STRAIGHT'
            else:
                return 'LEFT'

        def point_cmp(p1, p2):
            """Compares 2D points with regard to y
            coordinate value first, then x."""
            cmp_val = cmp(p1[1], p2[1])
            if cmp_val == 0:
                return cmp(p1[0], p2[0])
            else:
                return cmp_val

        num = len(points)
        if num < 3:
            raise Exception('Too few coordinates sent in.')

        # sort the coords according to y
        points = sorted(points.tolist(), cmp=point_cmp)

        # select the leftmost coord as the pivot
        pivot = points[0]
        coords = points[1:]

        # for remaining coords, sort them by polar angle
        # in counterclockwise order around pivot
        coords.sort(angle_cmp(pivot))

        # push the first three coords in a stack
        stack = [pivot, coords[0], coords[1]]

        # for the rest of the coords, while the angle formed by
        # the coord of the next-to-top of the stack, coord of
        # top of stack and the next coord makes a nonleft turn,
        # pop the stack
        # also, push the next coord into the stack at each loop
        for i in range(2, num - 1):
            while len(stack) >= 2 and \
                  turning(stack[-2], stack[-1], coords[i]) != 'LEFT':
                stack = stack[:-1]
            stack.append(coords[i])

        return np.array(stack)


def quickhull(sample):
        """Calculates the convex hull of an arbitrary 2D point cloud.

        This is a pure Python version of the Quick Hull algorithm.
        It's based on the version of ``literateprograms``, but fixes some
        old-style Numeric function calls.

        This version works with numpy version > 1.2.1

        References:

        * `Literateprograms <http://en.literateprograms.org/Quickhull_(Python,_arrays)>`_
        * `Wikipedia <http://en.wikipedia.org/wiki/QuickHull>`_

        Code adapted from:

        `<http://members.home.nl/wim.h.bakker/python/quickhull2d.py>`_

        :param sample: Points to which the convex hull is desired to be found.
        :type sample: :py:class:`numpy.ndarray`
        :return: The convex hull of the points.
        :rtype: :py:class:`numpy.ndarray`

        """

        def calculate_convex_hull(sample):
            link = lambda a, b: np.concatenate((a, b[1:]))
            edge = lambda a, b: np.concatenate(([a], [b]))

            def dome(sample, base):
                h, t = base
                dists = np.dot(sample-h, np.dot(((0, -1), (1, 0)), (t - h)))
                outer = np.repeat(sample, dists > 0, axis=0)

                if len(outer):
                    pivot = sample[np.argmax(dists)]
                    return link(dome(outer, edge(h, pivot)),
                                dome(outer, edge(pivot, t)))
                else:
                    return base

            if len(sample) > 2:
                axis = sample[:, 0]
                base = np.take(sample, [np.argmin(axis), np.argmax(axis)], axis=0)
                return link(dome(sample, base),
                            dome(sample, base[::-1]))
            else:
                return sample

        # Perform a reversal of points here to get points ordered clockwise instead of
        # counter clockwise that the QuickHull above returns.
        return calculate_convex_hull(sample)[::-1, :]


def sutherland_hodgman_polygon_clipping(subject_polygon, clip_polygon):
    """Sutherland-Hodgman polygon clipping.

    .. note

        This algorithm works in regular Cartesian plane, not in inverted y-axis image plane,
        so make sure that polygons sent in are ordered clockwise in regular Cartesian sense!

    Method reference:
    `Sutherland-Hodgman <http://en.wikipedia.org/wiki/Sutherland%E2%80%93Hodgman_algorithm>`_

    Reference code found at `Rosettacode
    <http://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping#Python>`_

    :param subject_polygon: A [n x 2] array of points representing the non-closed polygon to reduce.
    :type subject_polygon: :py:class:`numpy.ndarray`
    :param clip_polygon: A [m x 2] array of points representing the non-closed polygon to clip with.
    :type clip_polygon: :py:class:`numpy.ndarray`
    :return: A [r x 2] array of points representing the intersection polygon or :py:class:`None`
     if no intersection is present.
    :rtype: :py:class:`numpy.ndarray` or :py:class:`None`

    """
    TOLERANCE = 1e-14

    def inside(p):
        # This ``inside`` function assumes y-axis pointing upwards. If one would
        # like to rewrite this function to work with clockwise ordered coordinates
        # in the image style, then reverse the comparison from ``>`` to ``<``.
        return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (
        p[0] - cp1[0])

    def compute_intersection():
        dc = [cp1[0] - cp2[0], cp1[1] - cp2[1]]
        dp = [s[0] - e[0], s[1] - e[1]]
        n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
        n2 = s[0] * e[1] - s[1] * e[0]
        denominator = (dc[0] * dp[1] - dc[1] * dp[0])
        if np.abs(denominator) < TOLERANCE:
            # Lines were parallel.
            return None
        n3 = 1.0 / denominator
        return [(n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3]

    output_list = list(subject_polygon)
    cp1 = clip_polygon[-1]

    for clip_vertex in clip_polygon:
        cp2 = clip_vertex
        input_list = output_list
        if not input_list:
            return None
        output_list = []
        s = input_list[-1]

        for subject_vertex in input_list:
            e = subject_vertex
            if inside(e):
                if not inside(s):
                    intersection = compute_intersection()
                    if intersection is not None:
                        output_list.append(intersection)
                output_list.append(e)
            elif inside(s):
                intersection = compute_intersection()
                if intersection is not None:
                    output_list.append(intersection)
            s = e
        cp1 = cp2

    # TODO: Verify that points are clockwise sorted here.
    pnts_out = []
    while len(output_list):
        pnt = output_list.pop(0)
        if not any(
                [np.all(np.equal(pnt, unique_pnt)) for unique_pnt in pnts_out]):
            pnts_out.append(pnt)

    return np.array(pnts_out)
