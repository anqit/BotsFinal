zone_map = ["top left corner", "top edge", "top right corner", "left edge", "free space", "right edge", "bottom left corner", "bottom edge", "bottom left corner"]

class Bot:

    def __init__(self):

        self.minx = self.miny = 1000
        self.maxx = self.maxy = 0
        self.max_mag = 0.

        self.measurements = []
        self.magnitudes = []
        self.directions = []
        self.direction_deltas = []
        self.zones = []

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
    def find_zone(self, data_point, ox, oy):
        x, y = data_point

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
        offset_x = (self.maxx - self.minx) * .1
        offset_y = (self.maxy - self.miny) * .1

        for i in range(len(self.measurements)):
            data_point = self.measurements[i]
            zone = self.find_zone(data_point, offset_x, offset_y)
            self.zones.append(zone)

    def print_zones(self):
        for i in range(len(self.zones)):
            frame, x, y, zone = self.zones[i]
            print "f: ", frame, " x: ", x, " y: ", y, " zone: ", zone, " (", zone_map[zone - 1], ")"
