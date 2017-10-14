from typing import Tuple, Callable, List

import pygame
from pygame.surface import Surface
from pygame.rect import Rect

control_id = 0


class BaseControl:
    def __init__(self, dimensions: Rect, parent: Surface):
        global control_id
        self.id = control_id
        control_id += 1

        self.parent = parent
        self.dimensions: Rect = dimensions
        self.surface: Surface = Surface((dimensions.width, dimensions.height)).convert_alpha()

        self.mouse_entered = False
        self.focused = False
        self.left_down = False
        self.middle_down = False
        self.right_down = False

        self.keys_down = [False] * 127

    def handle(self):
        if pygame.key.get_focused():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_over = self.dimensions.collidepoint(mouse_x, mouse_y)

            (left_click_down, middle_click_down, right_click_down) = pygame.mouse.get_pressed()

            if mouse_over:
                if not self.mouse_entered:
                    self.mouse_entered = True
                    self.on_mouse_enter()

                if left_click_down != 0:
                    if not self.left_down:
                        self.left_down = True
                        self.on_mouse_down()
                    else:
                        self.left_down = True
                else:
                    if self.left_down:
                        self.left_down = False
                        self.on_mouse_up()
                        self.focused = True
                        self.on_mouse_click(mouse_x, mouse_y)
                        self.on_focus()
            else:
                if self.mouse_entered:
                    self.mouse_entered = False
                    self.on_mouse_leave()

                if left_click_down != 0:
                    if self.focused:
                        self.focused = False
                        self.on_blur()
                else:
                    if self.left_down:
                        self.left_down = False
                        self.on_mouse_up()
                        self.on_mouse_click_canceled()

            if self.focused:
                index = 0
                for key_pressed in pygame.key.get_pressed():
                    if index >= 127:
                        break

                    if key_pressed != 0:
                        if not self.keys_down[index]:
                            self.keys_down[index] = True

                            if pygame.key.get_mods() & pygame.KMOD_LSHIFT == pygame.KMOD_LSHIFT or pygame.key.get_mods() & pygame.KMOD_RSHIFT == pygame.KMOD_RSHIFT:
                                self.on_key_down(index, True)
                            else:
                                self.on_key_down(index, False)

                    else:
                        self.keys_down[index] = False
                    index += 1

        self.draw()

    def on_mouse_enter(self):
        print(self.id, "entered")

    def on_mouse_leave(self):
        print(self.id, "leave")

    def on_mouse_down(self):
        print(self.id, "mouse down")

    def on_mouse_up(self):
        print(self.id, "mouse up")

    def on_mouse_click_canceled(self):
        print(self.id, "canceled")

    def on_mouse_click(self, mouse_x, mouse_y):
        print(self.id, "clicked", mouse_x, mouse_y)

    def on_focus(self):
        print(self.id, "focus")

    def on_blur(self):
        print(self.id, "blur")

    def draw(self):
        self.parent.blit(self.surface, self.dimensions)

    def on_key_down(self, index: int, shift: bool):
        name = pygame.key.name(index)
        if shift:
            name = name.upper()
        print(name, str(index))


class Button(BaseControl):
    def __init__(self, parent: Surface, position: Tuple[int, int], text: str = '', width: int = 125):
        super().__init__(Rect(position[0], position[1], width, 25), parent)

        self.padding = 4
        self.text = text
        self.font = pygame.font.SysFont("monospace", 15)

        self.draw_control()

        self.on_click_events: List[Callable[[int, int], None]] = []

    def draw_control(self):
        top_left_rect = Rect(
            0, 0,
            self.dimensions.width - self.padding, self.dimensions.height - self.padding
        )
        bottom_right_rect = Rect(
            self.padding, self.padding,
            self.dimensions.width - self.padding, self.dimensions.height - self.padding
        )

        label = self.font.render(self.text, 1, color(255, 255, 255, 255))
        font_rect = Rect(
            (self.dimensions.width / 2) - (label.get_width() / 2),
            (self.dimensions.height / 2) - (label.get_height() / 2),
            self.dimensions.width,
            self.dimensions.height
        )

        if self.mouse_entered and self.left_down:
            font_rect = font_rect.move(self.padding / 2, self.padding / 2)
            self.surface.fill(color(0, 0, 200, 255), rect=bottom_right_rect)
            self.surface.fill(color(0, 0, 75, 255), rect=top_left_rect)
            self.surface.fill(color(0, 0, 250, 255),
                              rect=Rect(self.padding, self.padding, self.dimensions.width - self.padding * 2,
                                        self.dimensions.height - self.padding * 2))
        else:
            self.surface.fill(color(0, 0, 75, 255), rect=bottom_right_rect)
            self.surface.fill(color(0, 0, 200, 255), rect=top_left_rect)
            self.surface.fill(color(0, 0, 250, 255), rect=Rect(self.padding, self.padding, self.dimensions.width - self.padding * 2, self.dimensions.height - self.padding * 2))

        self.surface.blit(label, font_rect)

    def add_on_mouse_click(self, event: Callable[[int, int], None]):
        if event is not None:
            self.on_click_events.append(event)

    def on_mouse_click(self, mouse_x, mouse_y):
        for event in self.on_click_events:
            event(mouse_x, mouse_y)

    def on_mouse_enter(self):
        self.draw_control()

    def on_mouse_leave(self):
        self.draw_control()

    def on_mouse_down(self):
        self.draw_control()

    def on_mouse_up(self):
        self.draw_control()


class Input(BaseControl):
    def __init__(self, parent: Surface, position: Tuple[int, int], width: int = 200):
        super().__init__(Rect(position[0], position[1], width, 25), parent)

        self.padding = 2
        self.text = ''
        self.font = pygame.font.SysFont("monospace", 15)

        self.draw_control()

    def draw_control(self):
        if self.focused:
            self.surface.fill(color(50, 50, 255, 255))
        else:
            self.surface.fill(color(0, 0, 0, 255))
        text_area = Rect(self.padding, self.padding, self.dimensions.width - self.padding * 2, self.dimensions.height - self.padding * 2)
        self.surface.fill(color(255, 255, 255, 255), rect=text_area)

        font_area = Rect(self.padding * 2, self.padding * 2, self.dimensions.width - self.padding * 4, self.dimensions.height - self.padding * 4)
        text_to_render = self.text
        if self.focused:
            text_to_render += '|'
        label = self.font.render(text_to_render, 1, color(0, 0, 0, 255))
        self.surface.blit(label, font_area)

    def on_focus(self):
        self.draw_control()

    def on_blur(self):
        self.draw_control()

    def get_text(self) -> str:
        return self.text

    def set_text(self, text):
        self.text = text
        self.draw_control()

    def on_key_down(self, index: int, shift: bool):
        name = pygame.key.name(index)
        if name == "space":
            self.set_text(self.text + ' ')
        elif name == "backspace":
            if shift:
                self.set_text('')
            else:
                self.set_text(self.text[0:-1])
        elif name == "return":
            self.focused = False
            self.on_blur()
        elif len(name) == 1:
            if shift:
                if name == '-':
                    name = '_'
                elif name == '=':
                    name = "+"
                name = name.upper()
            self.set_text(self.text + name)
        else:
            print(name)


# noinspection PyArgumentList
def color(r: int, g: int, b: int, a: int = None):
    if a is None:
        return pygame.Color(r, g, b)
    return pygame.Color(r, g, b, a)