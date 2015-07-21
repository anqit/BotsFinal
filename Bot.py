from Util import *

zone_map = ["top left corner", "top edge", "top right corner", "left edge", "free space", "right edge", "bottom left corner", "bottom edge", "bottom left corner"]

class Bot:

    def __init__(self):

        self.minx = self.miny = 1000
        self.maxx = self.maxy = 0
        self.max_mag = 0.

        self.offset_x = (self.maxx - self.minx) * .1
        self.offset_y = (self.maxy - self.miny) * .1

        self.histo_x = 100
        self.histo_y = 100
        self.maxh = 0
        self.histogram = [[0 for i in range(self.histo_y)] for j in range(self.histo_x)]


        self.measurements = []
        self.magnitudes = []
        self.directions = []
        self.magnitude_deltas = []
        self.direction_deltas = []
        self.zones = []
        self.zone_behaviors = [[0., 0., 0.] for i in range(9)] # count, avg dv, avg dTheta per zone
        self.zone_errors = []

    def set_offsets(self, ox, oy):
        self.offset_x = ox
        self.offset_y = oy

    """
    ---------------> x
    |  minx           maxx
    |   --------------------- miny
    |   | 1 |     2     | 3 |
    |   |---|-----------|---| offset_y (oy)
    |   | 4 |     5     | 6 |
    |   |___|___________|___| offset_y (oy)
    |   | 7 |     8     | 9 |
    |   --------------------- maxy
    \/    offset_x (ox)
    y
    """
    def find_zone(self, data_point):
        x, y = data_point
        ox, oy = self.offset_x, self.offset_y

        if(x < self.minx + ox): # left side
            if(y < self.miny + oy): # top left corner
                return 1
            if(y > self.maxy - oy): # bottom left corner
                return 7
            else: # left edge
                return 4
        if(x > self.maxx - ox): # right side
            if(y < self.miny + oy): # top right corner
                return 3
            if(y > self.maxy - oy): # bottom right corner
                return 9
            else: # right edge
                return 6
        # otherwise, x is in middle (not on left or right edges)
        if(y < self.miny + oy): # top edge
            return 2
        if(y > self.maxy - oy): # bottom edge
            return 8
        else: # free space
            return 5

    def set_zones(self):
        for i in range(len(self.measurements)):
            data_point = self.measurements[i]
            zone = self.find_zone(data_point)

            c, v, T = self.zone_behaviors[zone - 1]
            c += 1
            v += self.magnitude_deltas[i]
            T += self.direction_deltas[i]
            self.zone_behaviors[zone - 1] = [c, v, T]

            self.zones.append(zone)

        for i in range(len(self.zone_behaviors)):
            c, dv, dT = self.zone_behaviors[i]
            dv /= c
            dT /= c
            self.zone_behaviors[i] = [c, dv, dT]

    def print_zones(self):
        for i in range(len(self.zones)):
            frame, x, y, zone = self.zones[i]
            print "f: ", frame, " x: ", x, " y: ", y, " zone: ", zone, " (", zone_map[zone - 1], ")"

    def set_histo(self):
        for i in range(len(self.measurements)):
            x, y = self.measurements[i]
            hx = self.getBucketX(x)
            hy = self.getBucketY(y)
            self.histogram[hx][hy] += 1
            self.maxh = max(self.maxh, self.histogram[hx][hy])

    def getBucketX(self, x):
        return self.getBucket(self.maxx, self.minx, self.histo_x, x)

    def getBucketY(self, y):
        return self.getBucket(self.maxy, self.miny, self.histo_y, y)

    def getBucket(self, max, min, num_buckets, val):
        return int((num_buckets - 1) * (float((val - min)) / float((max - min))))

    def print_hist(self):
        for row in range(len(self.histogram)):
            print self.histogram[row]

    def zone_predict(self, steps = 1, limit = 1002):
        if limit < 0:
            limit = len(self.measurements)

        self.zone_errors = [[0., 0.] for i in range(9)]

        for i in range(3, limit):
            x, y = self.measurements[i]
            magnitude = self.magnitudes[i]
            T = self.directions[i]
            zone = self.find_zone((x, y))
            c, dv, dT = self.zone_behaviors[zone - 1]

            new_mag = magnitude + dv
            new_T = truncate(T + dT)

            new_x = x + new_mag * cos(new_T)
            new_y = y + new_mag * sin(new_T)

            t, ze = self.zone_errors[zone - 1]
            t += 1
            ze += distance((self.measurements[i + 1]), (new_x, new_y))
            self.zone_errors[zone - 1] = [t, ze]

        ret = []
        for i in range(len(self.zone_errors)):
            t, ze = self.zone_errors[i]
            if t == 0:
                ret.append(0)
            else:
                ret.append(ze / t)
        return ret