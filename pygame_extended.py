import pygame
from helpers import Color


class Button:
    def __init__(self, text, font_size, pos, scale, color, callback):
        self.text = text
        self.font_size = font_size
        self.pos = pos
        self.scale = scale
        self.color = color
        self.callback = callback

        self.pos.x -= self.scale.x / 2 # to fix the centering

    def draw(self, screen):
        button = pygame.Rect(self.pos.x, self.pos.y, self.scale.x, self.scale.y)
        pygame.draw.rect(screen, self.color.value, button)  # draw button

        text_pos = self.pos + (self.scale // 2)
        txt = Text(self.text, self.font_size, text_pos)
        txt.draw(screen)

    # if cursor is over, call method
    def is_over(self, mouse_pos):
        if self.pos.x < mouse_pos[0] < self.pos.x + self.scale.x:
            if self.pos.y < mouse_pos[1] < self.pos.y + self.scale.y:
                self.callback(self)


class Text:
    def __init__(self, text, font_size, pos):
        self.text = text
        self.font_size = font_size
        self.pos = pos

    def draw(self, screen):
        font = pygame.font.Font('freesansbold.ttf', self.font_size)
        text = font.render(self.text, True, Color.white.value)
        text_rect = text.get_rect()
        text_rect.center = (self.pos.x, self.pos.y)
        screen.blit(text, text_rect)
