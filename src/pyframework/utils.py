from typing import Union

import pygame
from .ptypes import ColorType, RectType

def clamp(v: Union[int, float], mn: Union[int, float], mx: Union[int, float]):
    return max(min(v, mx), mn)


def img_clip(img: pygame.Surface, rect: tuple[int, int, int, int]):
    return img.subsurface(rect)


def color_swap(surf, old_color, new_color):
    clone = surf.copy()
    for x in range(surf.get_width()):
        for y in range(surf.get_height()):
            if clone.get_at((x, y)) == old_color:
                clone.set_at((x, y), new_color)
    return clone


def filled_surf(size: tuple[int,int], color: ColorType):
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf

def rect_at_center(rect: tuple[int,int, int, int]):
    return pygame.Rect((rect[0] - rect[2]/2, rect[1] - rect[3]/2, rect[2], rect[3]))

def lerp(mn, mx, amount):
    return ((mx-mn)*clamp(amount, 0, 1))+mn
