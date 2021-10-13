import os
from typing import Union

import pygame


def clamp(v: Union[int, float], mn: Union[int, float], mx: Union[int, float]):
    return max(min(v, mx), mn)


def img_clip(img: pygame.Surface, rect: tuple[int, int, int, int]):
    return img.subsurface(rect)
