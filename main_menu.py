import pygame
import game
from pygame import Vector2
from helpers import Color, PlayerType
import pygame_extended as gui


class MainMenu:
    def __init__(self):
        pygame.init() # initialize pygame
        self.running = True
        self.screen_size = Vector2(596, 596)
        self.screen = pygame.display.set_mode([int(self.screen_size.x), int(self.screen_size.y)])
        self.center = self.screen_size.x // 2

        self.current_screen = 0 # change when button pressed
        self.update_screen = True
        self.buttons = []

        self.team_btn_states = [PlayerType.none, PlayerType.human, PlayerType.ai]
        self.selected_players = {}

        self.update()

    def update(self):
        menu_txt = gui.Text("Menu", 32, Vector2(self.center, 50), Color.white.value)
        self.create_buttons()

        while self.running:
            if self.update_screen:
                menu_txt.draw(self.screen)
                self.draw_buttons()
                pygame.display.update()
                self.update_screen = False

            self.handle_input()
        pygame.quit()

    def create_buttons(self):
        btn_offset = 100
        blue_btn = gui.Button(self.team_btn_states[0], 20, Vector2(self.center - btn_offset, 200 - btn_offset), Vector2(100, 50), Color.blue, self.team_btn_clicked)
        red_btn = gui.Button(self.team_btn_states[0], 20, Vector2(self.center + btn_offset, 200 - btn_offset), Vector2(100, 50), Color.red, self.team_btn_clicked)
        yellow_btn = gui.Button(self.team_btn_states[0], 20, Vector2(self.center - btn_offset, 200), Vector2(100, 50), Color.yellow, self.team_btn_clicked)
        green_btn = gui.Button(self.team_btn_states[0], 20, Vector2(self.center + btn_offset, 200), Vector2(100, 50), Color.green, self.team_btn_clicked)
        start_btn = gui.Button("Start", 20, Vector2(self.center, 300), Vector2(100, 50), Color.black, self.start_game)
        self.buttons = [green_btn, yellow_btn, blue_btn, red_btn, start_btn]

    def draw_buttons(self):
        for button in self.buttons:
            button.draw(self.screen)

    def team_btn_clicked(self, button):
        index = self.team_btn_states.index(button.text)
        if index == len(self.team_btn_states) - 1:
            index = 0
        else:
            index += 1

        button.text = self.team_btn_states[index]
        self.selected_players[button.color] = self.team_btn_states[index]
        if self.selected_players[button.color] == self.team_btn_states[0]: # if it's None, remove it
            del self.selected_players[button.color]
        self.update_screen = True

    def start_game(self, button):
        game.Game(self.selected_players) # start the game
        self.running = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # close button
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.is_over(mouse_pos)

if __name__ == '__main__':
    MainMenu() # starts the menu
