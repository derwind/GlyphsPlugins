#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math

def solve_intersection(points):
    p0, p1, p2, p3 = points

    det = (p1.x-p0.x)*(p3.y-p2.y)-(p1.y-p0.y)*(p3.x-p2.x)
    if det == 0:
        p0, p1, p2, p3 = points2vectors(points)
        if (p1-p0)*(p3-p0) == 0 and (p2-p3)*(p0-p3) == 0:
            return float("inf"), float("inf")
        else:
            return None
    return ((p3.y-p2.y)*(p3.x-p0.x)-(p3.x-p2.x)*(p3.y-p0.y))/det, (-(p1.y-p0.y)*(p3.x-p0.x)+(p1.x-p0.x)*(p3.y-p0.y))/det

def dist(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def dist_pt_and_line(pt, a, b, c):
    """
    distance between pt and ax+by+c=0
    """

    return abs(a*pt.x+b*pt.y+c) / abs(a**2+b**2)

def cross_product(p1, p2):
    return p1.x*p2.y - p1.y*p2.x

def twenty_times_segment_area(points):
    if len(points) == 4:
        p0, p1, p2, p3 = points
        return 6*cross_product(p0, p1) + 3*cross_product(p0, p2) + cross_product(p0, p3) + 3*cross_product(p1, p2) + 3*cross_product(p1, p3) + 6*cross_product(p2, p3)
    else:
        p0, p1 = points
        return 10*cross_product(p0, p1)

def bezier(points, t):
    if t < 0 or t > 1:
        return None
    if len(points) == 4:
        p0, p1, p2, p3 = points
        x = (1-t)**3 * p0.x + 3*(1-t)**2 * t * p1.x + 3 * (1-t) * t**2 * p2.x + t**3 * p3.x
        y = (1-t)**3 * p0.y + 3*(1-t)**2 * t * p1.y + 3 * (1-t) * t**2 * p2.y + t**3 * p3.y
    else:
        p0, p1 = points
        x = (1-t) * p0.x + t * p1.x
        y = (1-t) * p0.y + t * p1.y
    return Vector(x, y)

def points2vectors(points):
    return [Vector(pt.x, pt.y) for pt in points]

class Vector(object):
    def __init__(self, x, y, do_round=False):
        if do_round:
            self.x = round(x)
            self.y = round(y)
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        return cross_product(self, other)

    def __repr__(self):
        return "<math2.Vector object x={} y={}>".format(self.x, self.y)
