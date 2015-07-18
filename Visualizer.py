__author__ = 'aprakash'

import turtle
from math import *

DIMX = 800.
DIMY = 600.
VECTOR_DIM = 50.

zone_color_map = ["red", "blue", "red", "blue", "green", "blue", "red", "blue", "red"]

def setup(bot):
    turtle.setup(DIMX, DIMY)
    window = turtle.Screen()
    window.bgcolor('white')

    # turtle.setworldcoordinates(0, 0, DIMX, DIMY)

    b = turtle.Turtle()
    b.radians()
    b.shape('arrow')
    b.color('green')
    b.resizemode('user')
    b.shapesize(0.5, 0.5, 0.5)
    b.penup()

    return window, b

def shift_scale(bot, index, scale):
    x, y = bot.measurements[index]
    x -= bot.minx # zero x's to bot.minx
    y -= bot.miny # zero y's to bot.miny

    # scale to fit in window
    x /= scale
    y /= scale

    # shift window origin to bottom left corner
    x -= DIMX / 2.
    y -= DIMY / 2.

    return x, y

def show_vectors(bot):
    window, b = setup(bot)

    for i in range(1, len(bot.magnitudes), 10):
        draw_vector(i, b, bot)

    window.exitonclick()

def show_path(bot):
    window, b = setup(bot)

    for i in range(len(bot.measurements)):
        draw_point(i, b, bot)

    window.exitonclick()

def draw_vector(index, trtl, bot):
    scale = get_scale(bot)
    x, y = shift_scale(bot, index, scale)

    zone = bot.zones[index]
    trtl.color(zone_color_map[zone - 1])

    mag = bot.magnitudes[index]
    dir = bot.directions[index]

    trtl.goto(x, y)
    trtl.setheading(dir) #/ 2. / pi * 360.)

    trtl.pendown()
    trtl.forward(mag / bot.max_mag * VECTOR_DIM)
    trtl.stamp()
    trtl.penup()

def draw_point(index, trtl, bot):
    scale = get_scale(bot)

    x, y = shift_scale(bot, index, scale)

    trtl.goto(x, y)
    trtl.pendown()

def get_scale(bot):
    return max((bot.maxx - bot.minx) / DIMX, (bot.maxy - bot.miny) / DIMY)