import pygame
from pygame import (
    Vector2
)

# builds and stores the paths
class Board:
    def __init__(self, screen_size):
        self.board_img = pygame.transform.scale(pygame.image.load('images/ludo.png'), (screen_size, screen_size))

        # declare the start positions of the different colors, these were calculated in gimp
        self.green_start = Vector2(554.5, 350)
        self.yellow_start = Vector2(247.3, 554.8)
        self.red_start = Vector2(349.7, 42.8)
        self.blue_start = Vector2(42.5, 247.6)

        # set the start position to the first item in the paths
        self.green_path = [self.green_start]
        self.yellow_path = [self.yellow_start]
        self.red_path = [self.red_start]
        self.blue_path = [self.blue_start]

        self.possible_moves = []

        # populate the path lists with the rest of the positions
        self.create_paths()

    def draw_board(self, screen):
        screen.blit(self.board_img, (0, 0))

    def create_paths(self):
        green_dir = ['left', 'down', 'left', 'up', 'left', 'up', 'right', 'up', 'right', 'down', 'right', 'down', 'left']
        yellow_dir = ['up', 'left', 'up', 'right', 'up', 'right', 'down', 'right', 'down', 'left', 'down', 'left', 'up']
        red_dir = ['down', 'right', 'down', 'left', 'down', 'left', 'up', 'left', 'up', 'right', 'up', 'right', 'down']
        blue_dir = ['right', 'up', 'right', 'down', 'right', 'down', 'left', 'down', 'left', 'up', 'left', 'up', 'right']

        dir_lists = [green_dir, yellow_dir, red_dir, blue_dir]
        paths = [self.green_path, self.yellow_path, self.red_path, self.blue_path]

        steps = [4, 4, 2, 4, 4, 2, 4, 4, 2, 4, 4, 1, 5] # how many steps before each turn
        step_amount = 51.2 # how many coordinates to move during a step, measured in gimp

        for i in range(4): # because there are 4 colors
            step_index = 0 #
            for axis in range(len(steps)):
                # get the direction vector
                dir_vector = self.get_direction_vector(dir_lists[i][axis])

                # for each step in the current axis, calculate the coordiantes
                for step in range(steps[axis]):
                    # add the step amount * direction to the previous path position
                    x = paths[i][step_index].x + (step_amount * dir_vector.x)
                    y = paths[i][step_index].y + (step_amount * dir_vector.y)

                    paths[i].append(pygame.math.Vector2(x, y))
                    step_index += 1

    def get_direction_vector(self, _dir):
        if _dir == 'left':
            return Vector2(-1, 0)
        elif _dir == 'right':
            return Vector2(1, 0)
        elif _dir == 'up':
            return Vector2(0, -1)
        elif _dir == 'down':
            return Vector2(0, 1)

