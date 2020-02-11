import pygame
import board
import player
import dice
from helpers import (
    StartPosition,
    Color,
    Team
)


class Game:
    def __init__(self, screen_size, colors):
        self.screen_size = screen_size
        # set up board
        self.running = True
        self.screen = pygame.display.set_mode([self.screen_size, self.screen_size])
        self.clock = pygame.time.Clock()
        self.board = board.Board(self.screen_size)
        self.dice = dice.Dice(self.screen, self.screen_size)

        self.all_players = []
        for color in colors.keys(): # add the color (player) if the color should play
            new_players = []
            for i in range(4):
                new_players.append(player.Player(StartPosition.get_pos(color)[i], self.get_path(color), color))
            self.all_players.append(new_players)

        self.current_playing = 0
        self.selected_player = None
        self.move_player = False

        self.update() # start the game loop

    def get_path(self, color):
        if color == Color.green:
            return self.board.green_path
        elif color == Color.yellow:
            return self.board.yellow_path
        elif color == Color.red:
            return self.board.red_path
        elif color == Color.blue:
            return self.board.blue_path

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
            # Input
            self.handle_input()
            # Logic
            self.throw_dice()
            self.player_action()

            # Render
            self.render()
            self.clock.tick(60)

        pygame.quit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # clo se button
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if not self.dice.completed_roll:
                    self.dice.start_roll()
                else: # check if a player has been clicked
                    for i in range(len(self.all_players)):
                        for player in self.all_players[i]:
                            mouse_pos = pygame.mouse.get_pos()
                            if player.is_over_player(mouse_pos):
                                self.selected_player = player
                            elif player.is_over_move(mouse_pos, self.dice.dice_num):
                                self.selected_player.currentPosIndex += self.dice.dice_num
                                self.move_player = True

    def player_action(self):
        if self.dice.completed_roll: # if the dice has been rolled, it can roll
            can_play = False
            for i in range(4): # check if the current playing is able to move (by checking each player unit)
                if self.all_players[self.current_playing][i].can_move(self.dice.dice_num):
                    can_play = True
                    break
            if can_play: # if it can play
                if self.selected_player is not None and not self.move_player: # check if has selected a player and not already moved
                    self.show_moves()
                elif self.move_player: # if the player has been moved and
                    self.selected_player.possible_moves.clear() # clear the move indicators
                    moved = self.selected_player.move_player() # move the player and store the result in 'moved'
                    if moved and not self.dice.double_roll: # when moved is true, go to the next player if it can't roll again
                        self.next_player()
                    elif moved: # play again, reset
                        self.double_roll_reset()
            else:
                self.next_player()

    def double_roll_reset(self):
        self.dice.completed_roll = False
        self.move_player = False
        self.selected_player = None
        self.clear_player_moves()

    def show_moves(self):
        self.clear_player_moves()
        if self.selected_player in self.all_players[self.current_playing]: # if the selected player is the currently playing
            self.selected_player.show_moves(self.dice.dice_num)

    def clear_player_moves(self):
        for player in self.all_players: # remove the other move indicators, so only one is shown at once
            for i in range(4):
                if player[i] != self.selected_player:
                    player[i].possible_moves.clear()

    def next_player(self): # reset
        self.selected_player = None
        self.move_player = False
        if self.current_playing == len(self.all_players) - 1:
            self.current_playing = 0
        else:
            self.current_playing += 1
        self.dice.completed_roll = False
        self.dice.double_roll = False

    def throw_dice(self):
        # DICE #
        current_team = Team.get_name(self.all_players[self.current_playing][0].color) # get the team name
        if not self.dice.completed_roll and not self.dice.roll: # if not rolling or have rolled
            self.dice.show_static_dice(current_team)
        # ROLL DICE #
        if self.dice.roll:
            self.dice.animate_dice(current_team)

    def render(self):
        # DRAW BOARD #
        self.board.draw_board(self.screen)
        # PLAYERS
        for i in range(len(self.all_players)):
            for player in self.all_players[i]:
                player.draw_player(self.screen)
                player.draw_moves(self.screen)
        # DICE
        if not self.dice.completed_roll: # if it hasn't been rolled, show it
            self.dice.draw_dice()
        pygame.display.update()







