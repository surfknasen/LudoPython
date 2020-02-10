import random
import pygame

class Dice:
    def __init__(self, screen, screen_size):
        self.images = ['images/dice1.png', 'images/dice2.png', 'images/dice3.png', 'images/dice4.png', 'images/dice5.png', 'images/dice6.png']

        self.screen = screen
        self.screen_size = screen_size
        self.center = (screen_size // 2) - 51.5 # calculate the screen center by using the screen size and half of the dice width/height

        self.roll_time = 3000 # ms
        self.roll_start = 0
        self.current_dice_img = self.images[0]
        self.current_team_color = ""
        self.roll = False # used from the main update loop to check whether to animate dice
        self.completed_roll = False

    def show_static_dice(self, current_team):
        self.completed_roll = False
        self.current_team_color = current_team

    def start_roll(self):
        self.roll = True
        self.roll_start = pygame.time.get_ticks()

    def animate_dice(self, current_team):
        time_since_roll = pygame.time.get_ticks() - self.roll_start
        if time_since_roll < self.roll_time:
            rand = random.randrange(0, 6)
            self.current_dice_img = self.images[rand]
        else:
            self.roll = False
            self.completed_roll = True
            pygame.time.wait(2000) # so that the player has time to see what number
            return

        # make it roll fast at the start and then slow down
        if time_since_roll > 500:
            pygame.time.wait(int(time_since_roll / 10))

    def draw_dice(self):
        self.transparent_background()
        self.current_player_text()
        img = pygame.image.load(self.current_dice_img)
        self.screen.blit(img, (self.center, self.center))

    def transparent_background(self):
        img = pygame.transform.scale(pygame.image.load('images/black_transparent.png'), (596, 596))
        self.screen.blit(img, (0, 0))

    def current_player_text(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        cur_team = "{0}'s turn".format(self.current_team_color)
        text = font.render(cur_team, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (self.screen_size // 2, self.center - 50)
        self.screen.blit(text, textRect)
