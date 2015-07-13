def read_data(f):
    data_points = []
    minx = 10000
    miny = 10000
    maxx = 0
    maxy = 0

    for line in f:
        data_point = [int(x.strip()) for x in line.split(',')]
        x, y = data_point

        maxx = max(maxx, x)
        minx = min(minx, x)
        maxy = max(maxy, y)
        miny = min(miny, y)

        data_points.append(data_point)

    return data_points, maxx, minx, maxy, miny


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
zone_map = ["top left corner", "top edge", "top right corner", "left edge", "free space", "right edge", "bottom left corner", "bottom edge", "bottom left corner"]
def find_zone(data_point, ox, oy, maxx, minx, maxy, miny):
    x, y = data_point

    if(x < minx + ox): # left side
        if(y < miny + oy): # top left corner
            return 1
        if(y > maxy - oy): # bottom left corner
            return 7
        else: # left edge
            return 4
    if(x > maxx - ox): # right side
        if(y < miny + oy): # top right corner
            return 3
        if(y > maxy - oy): # bottom right corner
            return 9
        else: # right edge
            return 6
    # otherwise, x is in middle (not on left or right edges)
    if(y < miny + oy): # top edge
        return 2
    if(y > maxy - oy): # bottom edge
        return 8
    else: # free space
        return 5

def print_zones(zones):
    for i in range(len(zones)):
        frame, x, y, zone = zones[i]
        print "f: ", frame, " x: ", x, " y: ", y, " zone: ", zone, " (", zone_map[zone - 1], ")"

f = open('training_data.txt', 'r')
data_points, maxx, minx, maxy, miny = read_data(f)

print "Max X: ", maxx
print "Min X: ", minx
print "Max Y: ", maxy
print "Min Y: ", miny

offset_x = (maxx - minx) * .1
offset_y = (maxy - miny) * .1

zones = []
for i in range(len(data_points)):
    data_point = data_points[i]
    zone = find_zone(data_point, offset_x, offset_y, maxx, minx, maxy, miny)
    zones.append([i, data_point[0], data_point[1], zone])

print_zones(zones)