# This simulates a player. I wanted it to look like a player, so it selects a player and then clicks the desired spot instead of moving instantly
import random
from pygame import Vector2, time


class BotController:
    def __init__(self, units, game_class):
        self.units = units
        self.game = game_class
        self.current_unit = self.units[0]
        self.clicked_unit = False
        self.move_to_pos = None

    def input(self):
        if self.game.dice.completed_roll and not self.clicked_unit:
            i = 0
            for unit in self.units:
                if unit.can_move(self.game.dice.dice_num):
                    i = self.units.index(unit)
                break
            self.current_unit = self.units[i]
            self.game.mouse_clicked(self.current_unit.pos)
            self.clicked_unit = True
        else:
            self.game.mouse_clicked(Vector2(0, 0))

    def move_unit(self):
        if self.move_to_pos is None and self.current_unit is not None:
            if len(self.current_unit.possible_moves) > 0:
                self.move_to_pos = self.current_unit.possible_moves[0]
            else: # try clicking again
                self.game.mouse_clicked(self.current_unit.pos)
        elif self.clicked_unit:
            self.game.mouse_clicked(self.move_to_pos)
            for pos in self.game.occupied_positions.values():
                if pos == self.move_to_pos:
                    self.clicked_unit = False
                    self.move_to_pos = None
                    self.current_unit = None

