import pygame
from helpers import Color
from pygame import Vector2
import math


class Player:
    def __init__(self, start_pos, path, color, game_class):
        self.start_pos = start_pos
        self.pos = Vector2(start_pos.x, start_pos.y)
        self.path = path
        self.color = color
        self.current_pos_index = -1
        self.start_scale = 7
        self.scale = self.start_scale
        self.game_class = game_class

        self.possible_moves = []

    def reset_player(self):
        print("reset")
        self.pos = Vector2(self.start_pos.x, self.start_pos.y)
        print(id(self.pos))
        print(id(self.start_pos))
        print("startPos {0} pos {1}".format(self.start_pos, self.pos)) # WTF
        self.current_pos_index = -1

    def move_player(self):
        if self.pos != self.path[self.current_pos_index]:
            dx, dy = (self.path[self.current_pos_index].x - self.pos.x, self.path[self.current_pos_index].y - self.pos.y)
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

    def is_over_move(self, mouse_pos, steps):
        scale = self.scale + 5
        for moves in self.possible_moves:
            sqx = (mouse_pos[0] - moves.x)**2
            sqy = (mouse_pos[1] - moves.y)**2
            if math.sqrt(sqx + sqy) < scale:
                return True
        return False

    def can_move(self, dice_num):
        if self.current_pos_index == -1:
            if dice_num == 1 or dice_num == 6:
                return self._spot_free(dice_num)
            else:
                return False
        return self._spot_free(dice_num)

    def _spot_free(self, dice_num):
        if self.path[self.current_pos_index + dice_num] not in self.game_class.occupied_positions.values():
            return True
        else:
            for player, pos in self.game_class.occupied_positions.items():
                if pos == self.path[self.current_pos_index + dice_num]:
                    if player.color == self.color:
                        return False
        return True

    def show_moves(self, dice_num):
        self.possible_moves.clear()
        if self.can_move(dice_num):
            self.possible_moves.append(self.path[self.current_pos_index + dice_num])
            if dice_num == 6 and self.current_pos_index == -1:
                self.possible_moves.append(self.path[0])
            self.scale = self.start_scale + 2

    def draw_moves(self, screen):
        for move in self.possible_moves:
            pygame.draw.circle(screen, Color.black.value, (int(move.x), int(move.y)), self.scale + 5)

