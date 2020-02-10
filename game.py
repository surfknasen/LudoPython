import pygame
import board
import player
import dice
from helpers import (
    StartPosition,
    Color,
)

class Game:

    def __init__(self, screen_size):
        self.screen_size = screen_size
        # set up board
        self.running = True
        self.screen = pygame.display.set_mode([self.screen_size, self.screen_size])
        self.clock = pygame.time.Clock()
        self.board = board.Board(self.screen_size)
        self.dice = dice.Dice(self.screen, self.screen_size)

        #TEMP
        self.green_players = []
        self.yellow_players = []
        self.red_players = []
        self.blue_players = []
        self.all_players = [self.green_players, self.yellow_players, self.red_players, self.blue_players]

        self.current_playing = 0

        self.create_players()
        self.update() # start the game loop

    #TEMP
    def create_players(self):
        for i in range(4):
            self.green_players.append(player.Player(StartPosition.green[i], self.board.green_path, Color.green, "Green"))
            self.yellow_players.append(player.Player(StartPosition.yellow[i], self.board.yellow_path, Color.yellow, "Yellow"))
            self.red_players.append(player.Player(StartPosition.red[i], self.board.red_path, Color.red, "Red"))
            self.blue_players.append(player.Player(StartPosition.blue[i], self.board.blue_path, Color.blue, "Blue"))

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
        current_team = self.all_players[self.current_playing][0].team # get the team name
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







