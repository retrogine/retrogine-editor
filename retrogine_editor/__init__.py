import pygame
import sys

from pygame.surface import Surface
from pygame.rect import Rect

from retrogine_editor.controls import *


class Application:
    def __init__(self):
        self.real_screen: Surface = None
        self.screen: Surface = None

    def run(self):
        pygame.init()
        pygame.mouse.set_visible(True)
        self.real_screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.screen = Surface((1280, 720))

        test1 = Input(self.screen, (10, 10))
        test2 = Button(self.screen, (10, 45), "Add")

        font = pygame.font.SysFont("monospace", 15)
        test2.add_on_mouse_click(lambda x, y: submitted_text.append(font.render(test1.get_text(), 1, color(0, 0, 0))))
        submitted_text = []

        while True:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.screen.fill((0, 155, 0))
            self.real_screen.fill((0, 0, 0))

            test1.handle()
            test2.handle()

            count = 0
            for text in submitted_text:
                self.screen.blit(text, Rect(10, (30 * count) + 100, 100, 100))
                count += 1

            real_size = (self.real_screen.get_width(), self.real_screen.get_height())
            self.real_screen.blit(
                pygame.transform.scale(self.screen, real_size),
                (0, 0)
            )
            pygame.display.flip()

    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Application().run()
