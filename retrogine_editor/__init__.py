from typing import Tuple, List

import pygame
import sys

from pygame.surface import Surface
from pygame.rect import Rect

from retrogine_editor.menu_item import MenuItem


class Application:
    def __init__(self, data_file_path: str):
        self.data_file_path = data_file_path
        self.real_screen: Surface = None
        self.screen: Surface = None
        self.menu_font: pygame.font.Font = None
        self.menu_items: List[MenuItem] = []
        self.states = ['menu']

    def run(self):
        pygame.init()
        pygame.mouse.set_visible(True)
        self.real_screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.screen = Surface((1280, 720))

        self.init_menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.states.append('exit')

            self.screen.fill((0, 0, 0))
            self.real_screen.fill((0, 0, 0))

            if self.states[-1] == 'menu':
                self.draw_menu()
            elif self.states[-1] == 'exit':
                self.quit()

            self.real_screen.blit(
                pygame.transform.scale(self.screen, (self.real_screen.get_width(), self.real_screen.get_height())),
                (0, 0))

            pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()

    def init_menu(self):
        center_x = self.screen.get_width() / 2
        start_y = 100
        height = 30
        index = 0

        self.menu_font = pygame.font.SysFont("monospace", 25)

        index += 1
        surface: Surface = self.menu_font.render('Palette Editor', 1, (255, 255, 255))
        rect: Rect = Rect(center_x - surface.get_width() / 2, start_y + (index * height), surface.get_width(), surface.get_height())
        self.menu_items.append(MenuItem('palette_editor', surface, rect))

        index += 1
        surface = self.menu_font.render('Sprite Editor', 1, (255, 255, 255))
        rect = Rect(center_x - surface.get_width() / 2, start_y + (index * height), surface.get_width(), surface.get_height())
        self.menu_items.append(MenuItem('sprite_editor', surface, rect))

        index += 1
        surface = self.menu_font.render('Map Editor', 1, (255, 255, 255))
        rect = Rect(center_x - surface.get_width() / 2, start_y + (index * height), surface.get_width(), surface.get_height())
        self.menu_items.append(MenuItem('map_editor', surface, rect))

        index += 1  # add some space

        index += 1
        surface = self.menu_font.render('Save', 1, (255, 255, 255))
        rect = Rect(center_x - surface.get_width() / 2, start_y + (index * height), surface.get_width(), surface.get_height())
        self.menu_items.append(MenuItem('save', surface, rect))

        index += 1
        surface = self.menu_font.render('Load', 1, (255, 255, 255))
        rect = Rect(center_x - surface.get_width() / 2, start_y + (index * height), surface.get_width(), surface.get_height())
        self.menu_items.append(MenuItem('load', surface, rect))

        index += 1  # add some space

        index += 1
        surface = self.menu_font.render('Exit', 1, (255, 255, 255))
        rect = Rect(center_x - surface.get_width() / 2, start_y + (index * height), surface.get_width(), surface.get_height())
        self.menu_items.append(MenuItem('exit', surface, rect))

    def draw_menu(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        left_click, middle_click, right_click = pygame.mouse.get_pressed()

        for menu_item in self.menu_items:
            rect = menu_item.rect

            if rect.collidepoint(mouse_x, mouse_y):
                if left_click == 1:
                    self.states.append(menu_item.state)

            self.screen.blit(menu_item.surface, rect)


if __name__ == "__main__":
    Application('/home/joeljohnson/dev/retrogine/retrogine-lib/test.data').run()
