import pygame
from helpers import Color
from pygame import Vector2
import math


class Unit:  # RENAME ALL PLAYER TO UNIT
    def __init__(self, start_pos, color, game_class):
        self.start_pos = start_pos
        self.pos = Vector2(start_pos.x, start_pos.y)
        self.color = color
        self.current_pos_index = -1
        self.start_scale = 12
        self.scale = self.start_scale
        self.game_class = game_class
        self.path = self.get_path(color)

        self.possible_moves = []

    def get_path(self, color):
        if color == Color.green:
            return self.game_class.board.green_path
        elif color == Color.yellow:
            return self.game_class.board.yellow_path
        elif color == Color.red:
            return self.game_class.board.red_path
        elif color == Color.blue:
            return self.game_class.board.blue_path

    def reset_player(self):
        self.pos = Vector2(self.start_pos.x, self.start_pos.y)
        self.current_pos_index = -1

    def move_player(self):
        if self.pos != self.path[self.current_pos_index]:
            dx, dy = (self.path[self.current_pos_index].x - self.pos.x, self.path[self.current_pos_index].y - self.pos.y)
            x_steps, y_steps = (dx / 3., dy / 3.)
            self.pos.x += x_steps
            self.pos.y += y_steps
        else:
            return True

    def is_over_player(self, mouse_pos):
        scale = self.scale + 7
        sqx = (mouse_pos[0] - self.pos.x)**2
        sqy = (mouse_pos[1] - self.pos.y)**2
        if math.sqrt(sqx + sqy) < scale:
            return True
        return False

    def is_over_move(self, mouse_pos):
        scale = self.scale + 7
        for move in self.possible_moves:
            sqx = (mouse_pos[0] - move.x)**2
            sqy = (mouse_pos[1] - move.y)**2
            if math.sqrt(sqx + sqy) < scale:
                return self.path.index(move)
        return False

    def can_move(self, spot_index):
        dice_num = self.game_class.dice.dice_num
        if self.current_pos_index == -1:
            if dice_num == 1 or dice_num == 6:
                return self.spot_free(spot_index)
            else:
                return False
        return self.spot_free(spot_index)

    def spot_free(self, spot_index):
        if self.path[spot_index] not in self.game_class.occupied_positions.values(): # list index out of range
            return True
        else: # check if the occupied spot is the same color
            for player, pos in self.game_class.occupied_positions.items():
                if pos == self.path[spot_index]:
                    if player.color == self.color:
                        return False
        return True

    def show_moves(self, dice_num):
        self.possible_moves.clear()
        if self.can_move(self.current_pos_index + dice_num):
            self.possible_moves.append(self.path[self.current_pos_index + dice_num])
            self.scale = self.start_scale + 2

        # if it's a number 6
        if dice_num == 6 and self.current_pos_index == -1:
            if self.can_move(0): # check if the first spot is taken
                self.possible_moves.append(self.path[0])

    def draw_player(self, screen):
        x = int(self.pos.x)
        y = int(self.pos.y)
        pygame.draw.circle(screen, Color.white.value, (x, y), self.scale + 2)
        pygame.draw.circle(screen, self.color.value, (x, y), self.scale)

    def draw_moves(self, screen):
        for move in self.possible_moves:
            pygame.draw.circle(screen, Color.white.value, (int(move.x), int(move.y)), self.scale + 2)

