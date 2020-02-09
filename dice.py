import random
import pygame

class Dice:
    def __init__(self, screen, screen_size):
        self.images = ['dice1.png', 'dice2.png', 'dice3.png', 'dice4.png', 'dice5.png', 'dice6.png']
        self.screen = screen
        self.center = (screen_size / 2) - 51.5 # calculate the screen center by using the screen size and half of the dice width/height

        self.roll_time = 3000 # ms
        self.roll_start = 0
        self.current_dice_img = self.images[0]
        self.roll = False # used from the main update loop to check whether to animate dice
        self.completed_roll = False

    def show_static_dice(self):
        img = pygame.image.load(self.images[0])
        self.screen.blit(img, (self.center, self.center))

    def start_roll(self):
        self.roll = True
        self.roll_start = pygame.time.get_ticks()

    def animate_dice(self):
        time_since_roll = pygame.time.get_ticks() - self.roll_start
        if time_since_roll < self.roll_time:
            rand = random.randrange(0, 6)
            self.current_dice_img = self.images[rand]
        else:
            self.roll = False
            self.completed_roll = True
            pygame.time.wait(2000) # so that the player has time to see what number
            return

        img = pygame.image.load(self.current_dice_img)
        self.screen.blit(img, (self.center, self.center))

        # make it roll fast at the start and then slow down
        if time_since_roll > 500:
            pygame.time.wait(int(time_since_roll / 10))
