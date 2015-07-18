from math import *
import csv
from Visualizer import *


# this is very inefficient for long lists...
def mean(list):
    return sum(list) / float(len(list))

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


class Bot:

    def __init__(self):

        self.minx = self.miny = 1000
        self.maxx = self.maxy = 0
        self.max_mag = 0.

        self.measurements = []
        self.magnitudes = []
        self.directions = []
        self.direction_deltas = []


bot = Bot()

with open("training_data.txt") as coordinates:
    for coordinate in coordinates:
        x, y = coordinate.strip().split(",")
        x = int(x)
        y = int(y)
        bot.measurements.append( (x, y) )
        
        mcount = len(bot.measurements)
        if mcount > 1:
            i = mcount - 2
    
            p1 = bot.measurements[i]
            p2 = bot.measurements[i + 1]
    
            magnitude = distance(p1, p2)
            bot.max_mag = max(bot.max_mag, magnitude)

            direction = heading(p1, p2)
    
            bot.magnitudes.append(magnitude)
            bot.directions.append(direction)

        dcount = len(bot.directions)
        if dcount > 1:
            i = dcount - 2
    
            d1 = bot.directions[i]
            d2 = bot.directions[i + 1]
    
            direction_delta = truncate(d2 - d1)
            bot.direction_deltas.append(direction_delta)

        bot.minx = min(x, bot.minx)
        bot.miny = min(y, bot.miny)
        bot.maxx = max(x, bot.maxx)
        bot.maxy = max(y, bot.maxy)

print "x range : ", bot.minx, " to ", bot.maxx
print "y range : ", bot.miny, " to ", bot.maxy

bot.magnitudes = [None] + bot.magnitudes
bot.directions = [None] + bot.directions
bot.direction_deltas =  [None, None] + bot.direction_deltas

# Thresholds
# ...

for i in range(len(bot.measurements)):

    # This is where the behavior detection should go.
    placeholder = 0

# with open('training_data.csv', 'wb') as csvfile:
#     write = csv.writer(csvfile)
#     for i in range(len(bot.measurements)):
#         write.writerow( [
#             bot.measurements[i][0],
#             bot.measurements[i][1],
#             bot.magnitudes[i],
#             bot.directions[i],
#             bot.direction_deltas[i],
#         ] )

# show_path(bot)
show_vectors(bot)