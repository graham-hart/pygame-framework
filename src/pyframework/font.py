from typing import Union

import pygame

from . import utils

default_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789?!.,:;\"'-+/\\_(){}<>^"


class Font:
    def __init__(self, char_surfs: list[pygame.Surface], font_size: int, color: tuple[int, int, int],
                 chars=default_chars):
        self.char_height = char_surfs[0].get_height() * font_size
        self.chars: dict[str, pygame.Surface] = {
            chars[i]: pygame.transform.scale(utils.color_swap(char_surfs[i], (0, 0, 0), color),
                                             (char_surfs[i].get_width() * font_size, self.char_height)) for i in
            range(len(chars))}

    def render(self, text: str, kerning: int = 1, space_width: int = 10, line_spacing: int = 4,
               background_color: Union[tuple[int, int, int], tuple[int, int, int, int]] = (0, 0, 0, 0)):
        text_lines = text.split("\n")
        target_surf = pygame.Surface(
            (self.text_width(text, kerning, space_width),
             self.text_height(text, line_spacing))).convert_alpha()
        target_surf.fill(background_color)
        y = 0
        for ln in text_lines:
            x = 0
            for char in ln:
                if char == ' ':
                    x += space_width
                elif char != '\r':
                    target_surf.blit(self.chars[char], (x, y))
                    x += self.chars[char].get_width() + kerning
            y += line_spacing + self.char_height
        return target_surf

    def text_width(self, text: str, kerning: int = 1, space_width: int = 10):
        max_width = 0
        for ln in text.split("\n"):
            width = -kerning
            for char in ln:
                if char == ' ':
                    width += space_width
                elif char != '\r':
                    img = self.chars[char]
                    width += img.get_width() + kerning
            max_width = max(width, max_width)
        return max_width

    def text_height(self, text: str, line_spacing: int = 4):
        return len(text.split("\n")) * (line_spacing + self.char_height) - line_spacing


def load(fn: str, size: int, color: tuple[int, int, int] = (0, 0, 0), sep_color: tuple[int, int, int] = (255, 0, 0),
         end_color: tuple[int, int, int] = (0, 255, 0),
         chars: str = default_chars):
    img = pygame.image.load(fn).convert_alpha()
    imgs = split_img(img, sep_color, end_color)
    return Font(imgs, size, color, chars)


def split_img(img: pygame.Surface, sep_color: tuple[int, int, int] = (255, 0, 0),
              end_color: tuple[int, int, int] = (0, 255, 0)):
    width, height = img.get_size()
    imgs = []
    i = 0
    while True:
        c = img.get_at((i, 0))
        if i >= width or c == end_color:
            break
        if c == sep_color:
            w = 0
            for x in range(i + 2, width):
                w += 1
                col = img.get_at((x, 0))
                if col == sep_color or col == end_color:
                    break
            imgs.append(img.subsurface(i + 1, 0, w, height))
            i += w - 1
        i += 1
    return imgs
