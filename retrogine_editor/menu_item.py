from pygame.surface import Surface
from pygame.rect import Rect


class MenuItem:
    def __init__(self, state: str, surface: Surface, rect: Rect):
        self.state = state
        self.surface = surface
        self.rect = rect
