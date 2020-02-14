import random
import pygame
from pygame import Vector2
from helpers import Color


class Dice:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.screen_size = screen_size
        self.center = (screen_size.y // 2) # calculate the screen center by using the screen size and half of the dice width/height
        self.current_playing = None

        self.roll_time = 500 # ms
        self.roll_start = 0
        self.dice_num = 1
        self.roll = False # used from the main update loop to check whether to animate dice
        self.double_roll = False
        self.completed_roll = False

    # display a static dice
    def show_static_dice(self, current_playing):
        self.completed_roll = False
        self.current_playing = current_playing

    # begins the dice roll
    def start_roll(self):
        self.roll = True
        self.roll_start = pygame.time.get_ticks()

    # animate the dice roll (flash the different numbers until one is picked)
    def animate_dice(self, current_playing):
        self.current_playing = current_playing
        time_since_roll = pygame.time.get_ticks() - self.roll_start
        if time_since_roll < self.roll_time:
            rand = random.randrange(1, 7) # 1 to 6
            self.dice_num = rand
        else:
            if self.double_roll is True:
                self.double_roll = False
            elif self.dice_num == 6:
                self.double_roll = True
            self.roll = False
            self.completed_roll = True
            self.current_playing = None
            pygame.time.wait(1000) # so that the player has time to see what number
            return

    def draw_dice(self):
        if self.current_playing is None:
            return
        self.transparent_background()
        self.current_player_text()
        self.build_dice(self.dice_num)

    # draw a transparent background behind the dice
    def transparent_background(self):
        transparent = pygame.Surface((1000, 1000)).convert_alpha()
        transparent.fill((0, 0, 0, 150))
        transparent_rect = transparent.get_rect()
        transparent_rect.center = (self.screen_size.y // 2, self.center)
        self.screen.blit(transparent, transparent_rect)

    # write text of the color of the current player
    def current_player_text(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        cur_team = "{0}'s turn".format(self.current_playing)
        text = font.render(cur_team, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.screen_size.y // 2, self.center - 80)
        self.screen.blit(text, text_rect)

    # FUNCTIONS FOR DRAWING THE ACTUAL DICE
    def build_dice_base(self):
        # draw white square
        scale = Vector2(100, 100)
        pos = Vector2(self.center-scale.x/2, self.center-scale.x/2)
        pygame.draw.rect(self.screen, Color.white.value, (pos.x, pos.y, scale.x, scale.y))
        return pos

    def build_dice(self, num):
        dice_center = self.build_dice_base()
        offset_x = [[50], [25, 75], [25, 50, 75], [25, 75, 25, 75], [25, 75, 25, 75, 50], [25, 75, 25, 75, 25, 75]] # for the dots
        offset_y = [[50], [25, 75], [25, 50, 75], [25, 25, 75, 75], [25, 25, 75, 75, 50], [25, 25, 75, 75, 50, 50]]
        for i in range(num):
            pos_x = int(dice_center.x) + offset_x[num-1][i]
            pos_y = int(dice_center.y) + offset_y[num-1][i]
            pygame.draw.circle(self.screen, Color.black.value, (pos_x, pos_y), 10)
