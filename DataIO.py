import csv

from Util import *
import Bot

def read_data():
    bot = Bot.Bot()

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

            magcount = len(bot.magnitudes)
            if magcount > 1:
                i = magcount - 2

                mag1 = bot.magnitudes[i]
                mag2 = bot.magnitudes[i + 1]

                magnitude_delta = mag2 - mag1
                bot.magnitude_deltas.append(magnitude_delta)

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

    bot.magnitudes = [0.] + bot.magnitudes
    bot.directions = [0.] + bot.directions
    bot.magnitude_deltas =  [0., 0.] + bot.magnitude_deltas
    bot.direction_deltas =  [0., 0.] + bot.direction_deltas

    bot.set_offsets((bot.maxx - bot.minx) * .07, (bot.maxy - bot.miny) * .07)
    bot.set_zones()
    bot.set_histo()

    return bot

def toCSV(bot):
    with open('training_data.csv', 'wb') as csvfile:
        write = csv.writer(csvfile)

        for i in range(len(bot.measurements)):
            write.writerow( [
                bot.measurements[i][0],
                bot.measurements[i][1],
                bot.magnitudes[i],
                bot.directions[i],
                bot.direction_deltas[i],
            ] )