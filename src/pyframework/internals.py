from typing import Union

import pygame

RectType = Union[
    tuple[int, int, int, int], tuple[tuple[int, int], tuple[int, int]], tuple[float, float, float, float], tuple[
        tuple[float, float], tuple[float, float]], pygame.Rect]
