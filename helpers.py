from enum import Enum
from pygame import Vector2


class PlayerType():
    none = "None"
    human = "Human"
    ai = "AI"

class Color(Enum):
    green = (0, 255, 0)
    dark_green = (0, 200, 0)
    yellow = (255, 255, 0)
    dark_yellow = (200, 200, 0)
    blue = (0, 0, 255)
    dark_blue = (0, 0, 200)
    red = (255, 0, 0)
    dark_red = (200, 0, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    beige = (249, 228, 183)
    brown = (206, 177, 128)


class Team:
    def get_name(color): # eg "Color.green". Removes the "Color." and returns "Green"
        return str(color).split(".")[-1].capitalize()


class StartPosition: # measured in gimp
    def get_pos(color):
        if color == Color.green:
            return [Vector2(503.8, 505), Vector2(555, 505), Vector2(503.8, 555), Vector2(555, 555)]
        elif color == Color.yellow:
            return [Vector2(92.2, 505), Vector2(41, 505), Vector2(92.2, 555), Vector2(41, 555)]
        elif color == Color.red:
            return [Vector2(503.8, 93), Vector2(555, 93), Vector2(503.8, 42), Vector2(555, 42)]
        elif color == Color.blue:
            return [Vector2(92.2, 93), Vector2(41, 93), Vector2(92.2, 42), Vector2(41, 42)]


