import pygame
from pygame import (
    Vector2
)
import board

pygame.init()

running = True
screen = pygame.display.set_mode([596, 596])
clock = pygame.time.Clock()

playing_board = board.Board()
boardImg = pygame.transform.scale(pygame.image.load('ludo.png'), (596, 596))

player_pos = playing_board.green_start
current_pos = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP: # DEBUGGING
            pos = pygame.mouse.get_pos()
            print("POS: " + str(pos))

    screen.fill((255, 255, 255))
    screen.blit(boardImg, (0, 0))

    #DEBUGGING, SHOWING PATH
    #for x in range(len(playing_board.green_path)):
    #    pygame.draw.circle(screen, (0, 255, 0), (int(playing_board.green_path[x].x), int(playing_board.green_path[x].y)), 10)
    #DEBUGGING, SHOWING PATH

    if player_pos != playing_board.green_path[current_pos]:
        dx, dy = (playing_board.green_path[current_pos].x - player_pos.x, playing_board.green_path[current_pos].y - player_pos.y)
        stepsx, stepsy = (dx / 2., dy / 2.)
        player_pos.x += stepsx
        player_pos.y += stepsy
    else:
        current_pos += 1

    pygame.draw.circle(screen, (0, 255, 0), (int(player_pos.x), int(player_pos.y)), 10)

    pygame.display.update()
    clock.tick(25)

# Done! Time to quit.
pygame.quit()
