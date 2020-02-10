import pygame
from helpers import Color
import math

class Player:
    def __init__(self, start_pos, path, color):
        self.pos = start_pos
        self.path = path
        self.color = color
        self.currentPosIndex = -1
        self.scale = 7

        self.possible_moves = []

    def move_player(self):
        if self.pos != self.path[self.currentPosIndex]:
            dx, dy = (self.path[self.currentPosIndex].x - self.pos.x, self.path[self.currentPosIndex].y - self.pos.y)
            x_steps, y_steps = (dx / 3., dy / 3.)
            self.pos.x += x_steps
            self.pos.y += y_steps
        else:
            return True

    def draw_player(self, screen):
        x = int(self.pos.x)
        y = int(self.pos.y)
        pygame.draw.circle(screen, Color.black.value, (x, y), self.scale + 5)
        pygame.draw.circle(screen, self.color.value, (x, y), self.scale)

    def is_over_player(self, mouse_pos):
        scale = self.scale + 5
        sqx = (mouse_pos[0] - self.pos.x)**2
        sqy = (mouse_pos[1] - self.pos.y)**2
        if math.sqrt(sqx + sqy) < scale:
            return True
        return False

    # WORK IN PROGRESS
    def show_moves(self, dice_num):
        self.possible_moves.clear()
        if self.currentPosIndex == -1: # if it's -1, it's not on the field
            if dice_num == 0: # 0 equals 1
                self.currentPosIndex = 0
                self.possible_moves.append(self.path[0])
            elif dice_num == 6:
                self.currentPosIndex = 0
                self.possible_moves.append(self.path[0])
                self.possible_moves.append(self.path[6])
        else:
            self.possible_moves.append(self.path[self.currentPosIndex + dice_num])

    def draw_moves(self, screen):
        for move in self.possible_moves:
            pygame.draw.circle(screen, Color.black.value, (int(move.x), int(move.y)), self.scale + 5)

    def is_over_move(self, mouse_pos, steps):
        scale = self.scale + 5
        for moves in self.possible_moves:
            sqx = (mouse_pos[0] - moves.x)**2
            sqy = (mouse_pos[1] - moves.y)**2
            if math.sqrt(sqx + sqy) < scale:
                return True
            return False
