import pygame
from pygame import Vector2
import board
import unit
import dice
import leaderboard
import bot_controller
from helpers import (
    StartPosition,
    PlayerType,
    Team,
)


class Game:
    def __init__(self, players):
        # set up board
        self.running = True
        self.screen_size = Vector2(800, 596)
        self.screen = pygame.display.set_mode([int(self.screen_size.x), int(self.screen_size.y)])
        self.lboard = leaderboard.Leaderboard(self.screen_size, self.screen)
        self.clock = pygame.time.Clock()
        self.board = board.Board(self.screen_size)
        self.dice = dice.Dice(self.screen, self.screen_size)
        self.occupied_positions = {}
        self.all_units = []
        self.bots = []
        self.current_playing_type = []

        for color in players.keys():  # add the color (player) if the color should play
            new_units = []
            for i in range(4):
                new_units.append(unit.Unit(StartPosition.get_pos(color)[i], color, self))
                self.occupied_positions[new_units[i]] = new_units[i].pos

            if players[color] == PlayerType.ai: # if it's AI, also add it to the bots list
                self.bots.append(bot_controller.BotController(new_units, self))
                self.current_playing_type.append(PlayerType.ai)
            else:
                self.bots.append(None)  # to make it easier to get the right bot from the bots list using the current_playing index
                self.current_playing_type.append(PlayerType.human)

            self.all_units.append(new_units)

        self.current_playing = 0
        self.selected_unit = None
        self.move_unit = False
        self.is_moving = False
        self.ai_playing = False

        self.update()  # start the game loop

    def update(self):
        """
        PSEUDOCODE:
        INPUT
        AI / PHYSICS - LOGIC
        RENDER

        1 Draw dice with click to roll
        2 Animate dice
        3 Show step amount
        4 Show available actions / Check player input
            - If player clicks on character, show where it can move to
            - If player clicks on spot it can move to, move there
        5 If player can move, move player
        6 If dice showed 6 and it's not the second roll:
            - Go back to 1
        7 Check if player on another character(s), if true: remove character(s), elif in goal: move character to goal
        8 Loop restarts
        """

        while self.running:
            self.ai_playing = self.current_playing_type[self.current_playing] is PlayerType.ai
            # Input
            self.handle_input()
            self.check_finished_units()

            if self.ai_playing:
                self.bots[self.current_playing].input()
                self.bots[self.current_playing].move_unit()

            self.player_action()
            self.throw_dice()

            # Render
            self.render()
            self.clock.tick(60)  # fps

        pygame.quit()

    # check inoput
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # close button
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_clicked(pygame.mouse.get_pos())

    # if the mouse has been clicked, start roll of handle player/unit input
    def mouse_clicked(self, mouse_pos):  # this is used by both the ai and player, therefore I want to pass in the mouse pos so the ai can simulate
        if not self.dice.completed_roll and not self.dice.roll:
            self.dice.start_roll()
        elif not self.is_moving:  # check if a player has been clicked
            self.player_input(mouse_pos)

    # show static or roll dice
    def throw_dice(self):
        try:
            current_team = Team.get_name(self.all_units[self.current_playing][0].color)  # get the team name
            if not self.dice.completed_roll and not self.dice.roll:  # if not rolling or have rolled
                self.dice.show_static_dice(current_team)
            elif self.dice.roll:
                self.dice.animate_dice(current_team)
        except:
            print("Failed to throw dice")

    # check if a unit has been clicked, if it has, select it and if a spot has been clicked, start the move
    def player_input(self, mouse_pos):
        if self.selected_unit is not None:  # check if a move was clicked
            clicked_spot = self.selected_unit.is_over_move(mouse_pos)  # returns False or the clicked spot index
            if clicked_spot is not False:
                self.selected_unit.current_pos_index = clicked_spot
                self.move_unit = True
                self.selected_unit.scale = self.selected_unit.start_scale
                return

        for i in range(len(self.all_units)):  # if it's not on a move position, check if a player was clicked
            for unit in self.all_units[i]:
                if unit.is_over_player(mouse_pos):
                    if self.selected_unit == unit and not self.ai_playing:  # unselect the player
                        self.selected_unit.scale = self.selected_unit.start_scale
                        self.selected_unit.possible_moves.clear()
                        self.selected_unit = None
                    else:
                        self.selected_unit = unit
                    return

    # moves the unit to the selected position, checks collision and goes to the next player when finished
    def player_action(self):
        if self.dice.completed_roll:  # if the dice has been rolled
            can_play = False
            for i in range(len(self.all_units[self.current_playing])):  # check if the current playing is able to move (by checking each player unit)
                spot_index = self.all_units[self.current_playing][i].current_pos_index + self.dice.dice_num
                if self.all_units[self.current_playing][i].can_move(spot_index):
                    can_play = True
                    break
            if can_play:  # if it can play
                if self.selected_unit is not None and not self.move_unit:  # check if has selected a player and not already moved
                    self.show_moves()
                elif self.move_unit and self.selected_unit is not None:
                    if len(self.selected_unit.possible_moves) > 0:
                        self.selected_unit.possible_moves.clear()  # clear the move indicators
                        del self.occupied_positions[self.selected_unit]
                    moved = self.selected_unit.move_player()  # move the player and store the result in 'moved'
                    self.is_moving = not moved
                    self.occupied_positions[self.selected_unit] = self.selected_unit.pos
                    if moved and not self.dice.double_roll:  # when moved is true, go to the next player if it can't roll again
                        self.check_collision()
                        self.next_player()
                    elif moved:  # play again, reset
                        self.check_collision()
                        self.double_roll_reset()
            else:
                self.next_player()

    # checks if a unit has reached the goal
    def check_finished_units(self):
        for i in range(len(self.all_units)):
            for unit in self.all_units[i]:
                if unit.pos == unit.path[len(unit.path) - 1]:
                    self.all_units[i].remove(unit)
                    self.lboard.add_point(unit.color, self)

    # if the player rolled a 6, roll another time
    def double_roll_reset(self):
        self.dice.completed_roll = False
        self.move_unit = False
        self.selected_unit = None
        self.check_unit_moves()

    # show the moves it can go to
    def show_moves(self):
        self.check_unit_moves()
        if self.selected_unit in self.all_units[self.current_playing]:  # if the selected player is the currently playing
            self.selected_unit.show_moves(self.dice.dice_num)

    def check_unit_moves(self):
        for unit in self.all_units:  # remove the other move indicators, so only one is shown at once
            for i in range(len(unit)):
                if unit[i] != self.selected_unit:
                    unit[i].scale = unit[i].start_scale
                unit[i].possible_moves.clear()

    #checks collision between two units, to knock out one
    def check_collision(self):  # check this before moving
        for unit in self.occupied_positions.keys():
            # check if they're the same positions
            if int(self.selected_unit.pos.x) == int(unit.pos.x) and int(self.selected_unit.pos.y) == int(unit.pos.y):
                if self.selected_unit.color != unit.color:
                    del self.occupied_positions[unit]
                    unit.reset_player()
                    return

    # resets so the next player can play
    def next_player(self):  # reset
        self.selected_unit = None
        self.move_unit = False
        if self.current_playing == len(self.all_units) - 1:
            self.current_playing = 0
        else:
            self.current_playing += 1
        self.dice.completed_roll = False
        self.dice.double_roll = False

    # render all ui
    def render(self):
        # DRAW BOARD #
        self.board.draw_board(self.screen, self.screen_size)
        # UNITS
        for i in range(len(self.all_units)):
            for player in self.all_units[i]:
                if not self.ai_playing:
                    player.draw_moves(self.screen)
                player.draw_player(self.screen)
        # DICE
        if not self.dice.completed_roll:  # if it hasn't been rolled, show it
            self.dice.draw_dice()
        # Leader board
        self.lboard.draw_leaderboard()
        pygame.display.update()
