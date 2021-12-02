from typing import Union

import pygame
from floatrect import FloatRect

IntTuple2 = tuple[int,int]
FloatTuple2 = tuple[float, float]
Vector2 = Union[IntTuple2, FloatTuple2, pygame.Vector2]

RectType = Union[
    tuple[int, int, int, int], tuple[IntTuple2, IntTuple2], tuple[float, float, float, float], tuple[
        FloatTuple2, FloatTuple2], pygame.Rect, FloatRect]

ColorType = Union[tuple[int,int,int], tuple[int,int,int,int], pygame.Color]
