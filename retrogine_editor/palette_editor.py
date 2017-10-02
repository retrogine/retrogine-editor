from typing import List, Tuple

import pygame
from pygame.surface import Surface
from pygame.rect import Rect

from retrogine_editor.input_box import ask


class PaletteSquare:
    def __init__(self, surface: Surface, rect: Rect, color: Tuple[int, int, int, int]):
        self.surface = surface
        self.rect = rect
        self.color = color


class PaletteEditor:
    def __init__(self, states: List[str]):
        self.states: List[str] = states
        self.main_palette: List[PaletteSquare] = []
        self.main_palette_size = 50
        self.click_up = False

        surface = Surface((self.main_palette_size, self.main_palette_size))
        surface.fill((0, 0, 150, 255))
        surface.fill((0, 0, 0, 255), rect=Rect(2, 2, self.main_palette_size - 4, self.main_palette_size - 4))
        pygame.draw.line(surface, (255, 255, 255, 255), (5, 5), (self.main_palette_size - 5, self.main_palette_size - 5))
        pygame.draw.line(surface, (255, 255, 255, 255), (self.main_palette_size - 5, 5), (5, self.main_palette_size - 5))
        self.main_palette_gb = surface

        default_color = (0, 0, 0, 0)
        for y in range(4):
            for x in range(4):
                surface = self.create_palette_square_surface(default_color)
                rect = Rect((x * (self.main_palette_size + 10) + 75, y * (self.main_palette_size +  10) + 100, self.main_palette_size, self.main_palette_size))
                self.main_palette.append(PaletteSquare(surface, rect, default_color))

    def draw(self, real_screen: Surface, screen: Surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        left_click, middle_click, right_click = pygame.mouse.get_pressed()

        count = 0
        screen.fill((0, 0, 0))
        for palette_square in self.main_palette:
            screen.blit(self.main_palette_gb, palette_square.rect)
            screen.blit(palette_square.surface, palette_square.rect)

            if palette_square.rect.collidepoint(mouse_x, mouse_y):
                if left_click == 1 and self.click_up:
                    self.click_up = False
                    result = ask(real_screen, 'R,G,B,A', default=",".join([str(x) for x in list(palette_square.color)]))
                    split = result.split(',')
                    if len(split) == 4:
                        split = [int(x) for x in split]
                        palette_square.color = tuple(split)

                        surface = self.create_palette_square_surface(palette_square.color)
                        palette_square.surface = surface

            count += 1

        if left_click == 0 and not self.click_up:
            self.click_up = True

        # self.states.pop()

    def create_palette_square_surface(self, color):
        surface = Surface((self.main_palette_size, self.main_palette_size)).convert_alpha()
        surface.fill((0, 0, 0, 0))
        surface.fill(color, rect=Rect(4, 4, self.main_palette_size - 8, self.main_palette_size - 8))
        return surface
