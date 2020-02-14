import random
from pygame import Vector2


# simulates a player's controls
class BotController:
    def __init__(self, units, game_class):
        self.units = units
        self.game = game_class
        self.current_unit = self.units[0]
        self.clicked_unit = False
        self.move_to_pos = None

    def input(self):
        if self.game.dice.completed_roll and not self.clicked_unit: # if the dice has been rolled and a unit hasn't been clicked
            self.select_unit()
            if self.current_unit is not None:
                self.game.mouse_clicked(self.current_unit.pos) # selct a unit
                self.clicked_unit = True
        else:
            self.game.mouse_clicked(Vector2(0, 0)) # click the screen to roll

    # select move position and move the unit
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

    # select the unit depending on the roll
    def select_unit(self):
        if self.game.dice.dice_num == 1 or self.game.dice.dice_num == 6: # if it's 1 or 6, check if there's a character at the start that can move
            for unit in self.units:
                if unit.current_pos_index == -1:
                    if unit.can_move(unit.current_pos_index + self.game.dice.dice_num):
                        i = self.units.index(unit)
                        self.current_unit = self.units[i]
                        return

        if self.current_unit is None: # if there's no character at the start that can move if it's 1 or 6, move another unit
            for unit in self.units:
                if unit.can_move(unit.current_pos_index + self.game.dice.dice_num):
                    i = self.units.index(unit)
                    self.current_unit = self.units[i]
                    return

    # select the position to move to depending on the roll
    def select_pos(self):
        for move in self.current_unit.possible_moves:
            for pos in self.game.occupied_positions.values():
                if pos == move:
                    self.move_to_pos = move
                    break
        if len(self.current_unit.possible_moves) > 1:
            rand = random.randrange(0, len(self.current_unit.possible_moves)-1)
        else:
            rand = 0
        self.move_to_pos = self.current_unit.possible_moves[rand]
