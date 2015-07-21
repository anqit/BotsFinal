from math import *

def distance(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def truncate(angle):
    """This maps all angles to a domain of [-pi, pi]"""
    while angle < 0.0:
        angle += pi * 2
    return ( (angle + pi) % (pi * 2) ) - pi

def heading(origin, target):
    """Returns the angle, in radians, between the two points"""
    ox, oy = origin
    tx, ty = target
    return truncate( atan2(ty - oy, tx - ox) )