import pygame
from pygame import Vector2
from helpers import Color, Team
import pygame_extended as gui

class Leaderboard:
    def __init__(self, screen_size, screen):
        self.screen_size = screen_size
        self.screen = screen
        self.points = {Color.blue : 0, Color.red : 0, Color.yellow : 0, Color.green : 0}
        self.ui_elements = []

    # draws the leaderboard, backdrop and title
    def draw_leaderboard(self):
        x = self.screen_size.y+100
        backdrop = pygame.Rect(self.screen_size.y, 0, x, self.screen_size.y)
        pygame.draw.rect(self.screen, Color.brown.value, backdrop) # draw backdrop
        title = gui.Text("Leaderboard", 26, Vector2(x, 20), Color.white.value)
        title.draw(self.screen)
        y = 50
        increment = 30
        for color in self.points.keys():
            score_text = gui.Text("{0} {1}".format(Team.get_name(color), self.points[color]), 20, Vector2(x, y), color.value)
            y += increment
            score_text.draw(self.screen)

    # add one point to the color that finished
    def add_point(self, color, game):
        self.points[color] += 1
        if self.points[color] == 4:
            print("Game finished.")
            game.running = False
