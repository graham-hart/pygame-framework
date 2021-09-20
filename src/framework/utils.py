import os
from typing import Union

import pygame


def load_image_dir(directory: str):
    imgs = {}
    d = os.fsencode(directory)
    for i, file in enumerate(os.listdir(d)):
        fn = os.fsdecode(file)
        imgs[os.path.splitext(fn)[0]] = pygame.image.load(
            f"./{directory}/{fn}").convert()
    return imgs

def clamp(v: Union[int, float], mn: Union[int, float], mx: Union[int, float]):
    return max(min(v, mx), mn)
