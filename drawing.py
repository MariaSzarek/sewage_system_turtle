"""
- rysowanie: obrys budynku, punkty, wspolrzedne

"""
import turtle

SPEED = 10

def offset(x, y, scale):
    offset_x = x / 2 * scale
    offset_y = y / 2 * scale
    return (offset_x, offset_y)

def draw_points(punkty, offset, scale, rozmiar=10):
    t = turtle.Turtle()
    t.speed(SPEED)
    t.penup()
    t.goto(punkty[0].x * scale - offset[0], punkty[0].y * scale - offset[1])
    for punkt in punkty:
        t.pendown()
        t.goto(punkt.x * scale - offset[0], punkt.y * scale - offset[1])
        t.dot(5)

def coordinates(punkty, offset, scale):
    t = turtle.Turtle()
    t.speed(SPEED)
    for punkt in punkty:
        t.penup()
        t.goto(punkt.x * scale - offset[0], punkt.y * scale - offset[1] - 20)
        t.pendown()
        t.write(f"({punkt.x}, {punkt.y})", align="center")

def draw_building(x, y, scale):
    t = turtle.Turtle()
    t.speed(SPEED)
    t.penup()
    t.goto(-x * scale / 2, -y * scale / 2)
    t.pendown()
    for _ in range(2):
        t.forward(x * scale)
        t.left(90)
        t.forward(y * scale)
        t.left(90)
    t.penup()