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
            self.select_unit()
            self.game.mouse_clicked(self.current_unit.pos)
            self.clicked_unit = True
        else:
            self.game.mouse_clicked(Vector2(0, 0))

    def move_unit(self):
        if self.move_to_pos is None and self.current_unit is not None:
            if len(self.current_unit.possible_moves) > 0:
                self.select_pos()
            else: # try clicking again
                self.game.mouse_clicked(self.current_unit.pos)
        elif self.clicked_unit:
            self.game.mouse_clicked(self.move_to_pos)
            for pos in self.game.occupied_positions.values():
                if pos == self.move_to_pos: # has moved and should reset
                    self.clicked_unit = False
                    self.move_to_pos = None
                    self.current_unit = None

    def select_unit(self):
        if self.game.dice.dice_num == 1 or self.game.dice.dice_num == 6:
            for unit in self.units:
                if unit.current_pos_index == -1:
                    if unit.can_move(unit.current_pos_index + self.game.dice.dice_num):
                        print(unit.pos)
                        i = self.units.index(unit)
                        self.current_unit = self.units[i]
                        print("can move")
                        return

        if self.current_unit is None:
            for unit in self.units:
                if unit.can_move(unit.current_pos_index + self.game.dice.dice_num):
                    i = self.units.index(unit)
                    self.current_unit = self.units[i]
                    return
        """
        for unit in self.units:
            if self.game.dice.dice_num == 1 or self.game.dice.dice_num == 6:
                if unit.current_pos_index == -1:
                    if unit.can_move(self.game.dice.dice_num):
                        i = self.units.index(unit)
                        break
            elif unit.can_move(self.game.dice.dice_num):
                i = self.units.index(unit)
                break
        """

    def select_pos(self):
        #self.move_to_pos = self.current_unit.possible_moves[0]
        for move in self.current_unit.possible_moves:
            for pos in self.game.occupied_positions.values():
                if pos == move:
                    self.move_to_pos = move
                    break
        if len(self.current_unit.possible_moves) > 1:
            rand = random.randrange(0, len(self.current_unit.possible_moves)-1)
        else:
            rand = 0

        print("selected pos")
        self.move_to_pos = self.current_unit.possible_moves[rand]

