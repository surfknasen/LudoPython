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
            self.move_player()

            # Render
            self.render()
            self.clock.tick(60)

        pygame.quit()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # clo se button
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dice.start_roll()

    def move_player(self):
        # DRAW PLAYERS - TEMP
        for i in range(len(self.all_players)):
            for player in self.all_players[i]:
                if self.dice.completed_roll:
                    player.move_player(1)

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
        # DICE
        if not self.dice.completed_roll: # if it hasn't been rolled, show it
            self.dice.draw_dice()
        pygame.display.update()







