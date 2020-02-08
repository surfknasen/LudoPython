import pygame
from pygame import (
    Vector2
)

class Player:
    def __init__(self, color, start_pos):
        self.color = color
        self.position = start_pos
        self.currentPosIndex = 0

    def movePlayer(self, steps_to_move, path):
        if self.position != path[self.currentPosIndex]:
            dx, dy = (path[self.currentPosIndex].x - self.position.x, path[self.currentPosIndex].y - self.position.y)
            x_steps, y_steps = (dx / 3., dy / 3.)
            self.position.x += x_steps
            self.position.y += y_steps
        else:
            self.currentPosIndex += steps_to_move

    def drawPlayer(self, screen):
        x = int(self.position.x)
        y = int(self.position.y)
        pygame.draw.circle(screen, (0, 255, 0), (x, y), 10)
