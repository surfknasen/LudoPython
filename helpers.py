from pygame import (
    Vector2
)

class Color():
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)

class StartPosition(): # measured in gimp
    green = [Vector2(503.8, 505), Vector2(555, 505), Vector2(503.8, 555), Vector2(555, 555)]
    yellow = [Vector2(92.2, 505), Vector2(41, 505), Vector2(92.2, 555), Vector2(41, 555)]
    red = [Vector2(503.8, 93), Vector2(555, 93), Vector2(503.8, 42), Vector2(555, 42)]
    blue = [Vector2(92.2, 93), Vector2(41, 93), Vector2(92.2, 42), Vector2(41, 42)]
