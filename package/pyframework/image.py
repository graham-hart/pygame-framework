import os

import pygame


def load_dir(directory: str):
    imgs = {}
    d = os.fsencode(directory)
    for file in os.listdir(d):
        fn = os.fsdecode(file)
        if fn.endswith(".jpg") or fn.endswith(".png") or fn.endswith("jpeg"):
            imgs[os.path.splitext(fn)[0]] = load(f"./{directory}/{fn}")
    return imgs


def load(path: str):
    return pygame.image.load(path).convert()


def load_all(directory:str):
    imgs = {}
    files = [entry.path.strip("./") for entry in [f for f in os.scandir(directory)] if entry.is_file()]
    for i in files:
        if i.endswith(".jpg") or i.endswith(".png") or i.endswith("jpeg"):
            imgs[os.path.splitext(i)[0]] = load(i)
    return imgs
