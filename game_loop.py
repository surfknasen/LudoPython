import pygame
import board
import player
from helpers import (
    Color
)

pygame.init()

running = True
screen = pygame.display.set_mode([596, 596])
clock = pygame.time.Clock()

game_board = board.Board()
boardImg = pygame.transform.scale(pygame.image.load('ludo.png'), (596, 596))

green_player = player.Player(Color.green, game_board.green_start)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            print("down")

    screen.fill((255, 255, 255))
    screen.blit(boardImg, (0, 0))

    green_player.movePlayer(6, game_board.green_path)
    green_player.drawPlayer(screen)

    #DEBUGGING, SHOWING PATH
    #for x in range(len(playing_board.green_path)):
    #    pygame.draw.circle(screen, (0, 255, 0), (int(playing_board.green_path[x].x), int(playing_board.green_path[x].y)), 10)
    #DEBUGGING, SHOWING PATH

    pygame.display.update()
    clock.tick(30)

# Done! Time to quit.
pygame.quit()
