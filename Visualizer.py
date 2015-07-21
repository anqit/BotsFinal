__author__ = 'aprakash'

import turtle
from math import *

DIMX = 800.
DIMY = 600.
VECTOR_DIM = 50.

zone_color_map = ["red", "blue", "red", "blue", "green", "blue", "red", "blue", "red"]

def setup(bot):
    global scale
    scale = get_scale(bot)

    turtle.setup(DIMX, DIMY)
    window = turtle.Screen()
    window.bgcolor('white')
    window.colormode(255)

    # turtle.setworldcoordinates(0, 0, DIMX, DIMY)
    turtle.tracer(10, 1)
    draw_lines(bot)

    b = turtle.Turtle()
    b.radians()
    b.shape('arrow')
    b.color('green')
    b.resizemode('user')
    b.shapesize(0.5, 0.5, 0.5)
    b.penup()

    return window, b

def draw_lines(bot):
    ox, oy = scale_dim(bot.offset_x , bot.offset_y)
    dx, dy = scale_dim(bot.maxx - bot.minx, bot.maxy - bot.miny)

    lines = turtle.Turtle()
    lines.penup()

    # draw outlines
    lines.width(5.)
    lines.color("black")
    drawV(lines, 0, dy)
    drawV(lines, dx, dy)
    drawH(lines, 0, dx)
    drawH(lines, dy, dx)

    # draw zone lines
    lines.penup()
    lines.width(1.)
    lines.color("purple")
    drawV(lines, ox, dy)
    drawV(lines, dx - ox, dy)
    drawH(lines, oy, dx)
    drawH(lines, dy - oy, dx)

# draw vertical line at x
def drawV(trtl, x_coord, max = DIMY):
    draw_line(trtl, (x_coord, 0), (x_coord, max))

# draw horizontal line at y
def drawH(trtl, y_coord, max = DIMX):
    draw_line(trtl, (0, y_coord), (max, y_coord))

# draw line from p1 to p2
def draw_line(trtl, p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    trtl.penup()
    trtl.goto(shift(x1, y1))
    trtl.pendown()
    trtl.goto(shift(x2, y2))

    trtl.penup()

def shift(x, y):
    x -= DIMX / 2.
    y -= DIMY / 2.

    return x, y

def scale_dim(x, y):
    x /= scale
    y /= scale

    return x, y

def bot_scale_shift(x, y, bot):
    x -= bot.minx # zero x's to bot.minx
    y -= bot.miny # zero y's to bot.miny

    # scale to fit in window
    x, y = scale_dim(x, y)

    # shift window origin to bottom left corner
    x, y = shift(x, y)

    return x, y

def show_vectors(bot, granularity = 10):
    window, b = setup(bot)

    for i in range(1, len(bot.magnitudes), granularity):
        draw_vector(i, b, bot)

    window.exitonclick()

def show_path(bot):
    window, b = setup(bot)

    for i in range(len(bot.measurements)):
        draw_point(i, b, bot)

    window.exitonclick()

def draw_vector(index, trtl, bot):
    x, y = bot.measurements[index]
    x, y = bot_scale_shift(x, y, bot)

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
    x, y = bot.measurements[index]
    x, y = bot_scale_shift(x, y, bot)

    zone = bot.zones[index]
    trtl.color(zone_color_map[zone - 1])
    trtl.goto(x, y)
    trtl.pendown()

def get_scale(bot):
    return max((bot.maxx - bot.minx) / DIMX, (bot.maxy - bot.miny) / DIMY)

def show_histo(bot):
    window, b = setup(bot)
    b.shape("square")
    dx, dy = scale_dim(DIMX / bot.histo_x, DIMY / bot.histo_y)
    b.shapesize(dx, dy)

    H = bot.histogram

    for row in range(len(H)):
        for col in range(len(H[0])):
            b.penup()
            x, y = shift(col * DIMX / scale / bot.histo_x, row * DIMY / scale / bot.histo_y)
            b.goto(x, y)
            intensity = min(255, 255. * H[row][col] / bot.maxh + 20)
            b.color(intensity, intensity, intensity)
            b.stamp()

    window.exitonclick()