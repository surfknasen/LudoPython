import random
import pygame


class Dice:
    def __init__(self, screen, screen_size):
        self.images = ['images/dice1.png', 'images/dice2.png', 'images/dice3.png', 'images/dice4.png', 'images/dice5.png', 'images/dice6.png']

        self.screen = screen
        self.screen_size = screen_size
        self.center = (screen_size.y // 2) - 51.5 # calculate the screen center by using the screen size and half of the dice width/height
        self.current_playing = None

        self.roll_time = 100 # ms
        self.roll_start = 0
        self.dice_img = self.images[0]
        self.dice_num = 0
        self.roll = False # used from the main update loop to check whether to animate dice
        self.double_roll = False
        self.completed_roll = False

    def show_static_dice(self, current_playing):
        self.completed_roll = False
        self.current_playing = current_playing

    def start_roll(self):
        self.roll = True
        self.roll_start = pygame.time.get_ticks()

    def animate_dice(self, current_playing):
        self.current_playing = current_playing
        time_since_roll = pygame.time.get_ticks() - self.roll_start
        if time_since_roll < self.roll_time:
            rand = random.randrange(1, 7) # 1 to 6
            self.dice_num = rand
            self.dice_img = self.images[rand-1]
        else:
            self.dice_num = 6
            if self.double_roll is True:
                self.double_roll = False
            elif self.dice_num == 6:
                self.double_roll = True
            self.roll = False
            self.completed_roll = True
            self.current_playing = None
            pygame.time.wait(1000) # so that the player has time to see what number
            return

        # make it roll fast at the start and then slow down
       # if time_since_roll > 500:
         #   pygame.time.wait(int(time_since_roll / 10))

    def draw_dice(self):
        if self.current_playing is None:
            return
        self.transparent_background()
        self.current_player_text()
        img = pygame.image.load(self.dice_img)
        self.screen.blit(img, (self.center, self.center))

    def transparent_background(self):
        transparent = pygame.Surface((1000, 1000)).convert_alpha()
        transparent.fill((0, 0, 0, 150))
        transparent_rect = transparent.get_rect()
        transparent_rect.center = (self.screen_size.y // 2, self.center)
        self.screen.blit(transparent, transparent_rect)

    def current_player_text(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        cur_team = "{0}'s turn".format(self.current_playing)
        text = font.render(cur_team, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.screen_size.y // 2, self.center - 50)
        self.screen.blit(text, text_rect)
