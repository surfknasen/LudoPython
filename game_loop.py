import pygame
import random
import board
import player
import dice
from pygame import (
    Vector2
)
from helpers import (
    StartPosition,
    Color
)

class Game:
    def __init__(self):
        pygame.init() # initialize pygame
        self.screen_size = 596

        # set up board
        self.running = True
        self.screen = pygame.display.set_mode([self.screen_size, self.screen_size])
        self.clock = pygame.time.Clock()
        self.board = board.Board(self.screen_size)

        self.green_players = []
        self.yellow_players = []
        self.red_players = []
        self.blue_players = []
        self.all_players = [self.green_players, self.yellow_players, self.red_players, self.blue_players]
        self.create_players()

        self.create_players()
        self.update() # start the game loop

    def create_players(self):
        for i in range(4):
            self.green_players.append(player.Player(StartPosition.green.value[i], self.board.green_path, Color.green))
            self.yellow_players.append(player.Player(StartPosition.yellow.value[i], self.board.yellow_path, Color.yellow))
            self.red_players.append(player.Player(StartPosition.red.value[i], self.board.red_path, Color.red))
            self.blue_players.append(player.Player(StartPosition.blue.value[i], self.board.blue_path, Color.blue))

    def update(self):
        """
        PSEUDOCODE:
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

        _dice = dice.Dice(self.screen, self.screen_size)

        while self.running:
            # DRAW BOARD #
            self.board.draw_board(self.screen)
            # DICE #
            if not _dice.completed_roll and not _dice.roll:
                _dice.show_static_dice()

            # INPUT #
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # close button
                    self.running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    _dice.start_roll()

            # ROLL DICE #
            if _dice.roll:
                _dice.animate_dice()

            for i in range(len(self.all_players)):
                for player in self.all_players[i]:
                    if _dice.completed_roll:
                        player.movePlayer(1)
                    player.drawPlayer(self.screen)
            #green_player.movePlayer(1, self.board.green_path)
            #green_player.drawPlayer(self.screen)

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()

if __name__ == '__main__':
    game = Game() # starts the game









