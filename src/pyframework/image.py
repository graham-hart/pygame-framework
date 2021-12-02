import os

import pygame


def load_filenames(directory: str):
    imgs = {}
    d = os.fsencode(directory)
    for file in os.listdir(d):
        fn = os.fsdecode(file)
        if fn.endswith(".jpg") or fn.endswith(".png") or fn.endswith("jpeg"):
            imgs[os.path.splitext(fn)[0]] = load(f"./{directory}/{fn}")
    return imgs


def load(path: str):
    return pygame.image.load(path).convert_alpha()


def _load_dir_recursive(directory:str):
    imgs = {}
    directories = [entry.path.strip("./") for entry in [f for f in os.scandir(directory)] if entry.is_dir()]
    files = [entry.path.strip("./") for entry in [f for f in os.scandir(directory)] if entry.is_file()]
    for i in files:
        if i.endswith(".jpg") or i.endswith(".png") or i.endswith("jpeg"):
            imgs[os.path.splitext(i)[0]] = load(i)
    for i in directories:
        imgs.update(_load_dir_recursive(i))
    return imgs

def load_dir_recursive(directory: str, scale=None):
    return {k[len(directory)+1:]: pygame.transform.scale(v, (scale, scale)) if scale else v for k,v in _load_dir_recursive(directory).items()}
