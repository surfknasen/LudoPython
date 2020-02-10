import pygame
import game
from pygame import (
    Vector2
)
import pygame_extended as gui


class MainMenu:
    def __init__(self):
        pygame.init() # initialize pygame
        self.running = True
        self.screen_size = 596
        self.screen = pygame.display.set_mode([self.screen_size, self.screen_size])
        self.center = self.screen_size // 2

        self.current_screen = 0 # change when button pressed
        self.draw_next_screen = True
        self.screens = [self.choose_play_type]
        self.buttons = []

        self.update()

    def update(self):
        while self.running:
            if self.draw_next_screen:
                self.screens[self.current_screen]()
                self.draw_next_screen = False
                pygame.display.update()

            self.handle_input()
        pygame.quit()

    def choose_play_type(self):
        center = self.center

        menu_txt = gui.Text("Menu", 32, Vector2(center, center - 50))
        menu_txt.draw(self.screen)
        ai_btn = gui.Button("Ai", 20, Vector2(center - 100, center), Vector2(100, 50), self.ai_btn_clicked)
        ai_btn.draw(self.screen)
        friends_btn = gui.Button("Friends", 20, Vector2(center + 100, center), Vector2(100, 50), self.friends_btn_clicked)
        friends_btn.draw(self.screen)

        self.buttons.append(ai_btn)
        self.buttons.append(friends_btn)

    def ai_btn_clicked(self):
        print("AI CLICKED")

    def friends_btn_clicked(self):
        print("FRIENDS CLICKED")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close button
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.is_over(mouse_pos)
                        #_game = game.Game(self.screen_size)
                        #return

if __name__ == '__main__':
    MainMenu() # starts the menu
