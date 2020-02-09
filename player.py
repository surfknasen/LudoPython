import pygame

class Player:
    def __init__(self, start_pos, path, color):
        self.position = start_pos
        self.path = path
        self.color = color
        self.currentPosIndex = 0

    def movePlayer(self, steps_to_move):
        if self.position != self.path[self.currentPosIndex]:
            dx, dy = (self.path[self.currentPosIndex].x - self.position.x, self.path[self.currentPosIndex].y - self.position.y)
            x_steps, y_steps = (dx / 3., dy / 3.)
            self.position.x += x_steps
            self.position.y += y_steps
        else:
            self.currentPosIndex += steps_to_move

    def drawPlayer(self, screen):
        x = int(self.position.x)
        y = int(self.position.y)
        pygame.draw.circle(screen, self.color.value, (x, y), 10)
