import pygame
from pygame import Vector2
from helpers import Color
import pygame_extended as gui


class Leaderboard:
    def __init__(self, screen_size, screen):
        self.screen_size = screen_size
        self.screen = screen

    def draw_leaderboard(self):
        x = self.screen_size.x - self.screen_size.y
        backdrop = pygame.Rect(self.screen_size.y, 0, x, self.screen_size.y)
        pygame.draw.rect(self.screen, Color.brown.value, backdrop)  # draw button

        title = gui.Text("Leaderboard", 26, Vector2(self.screen_size.y+100, 20), Color.white.value)
        title.draw(self.screen)
