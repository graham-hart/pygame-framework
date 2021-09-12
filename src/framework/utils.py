import json
import os
from typing import Union

import pygame as pg


def load_image_dir(directory: str):
    imgs = {}
    d = os.fsencode(directory)
    for i, file in enumerate(os.listdir(d)):
        fn = os.fsdecode(file)
        imgs[os.path.splitext(fn)[0]] = pg.image.load(f"./{directory}/{fn}").convert()
    return imgs


def parse_map_key(key: str):
    return tuple(int(i) for i in key.split(","))


def format_map_key(loc: tuple[int, int]):
    return f"{loc[0]},{loc[1]}"


def read_map(fn: str) -> dict[str, dict[str, str]]:
    path = f"./{fn}"
    if os.path.exists(path):
        with open(path, "r+") as file:
            data = file.read()
            return json.loads(data) if data != "" else {}
    else:
        f = open(path, "x")
        f.close()
        return {}


def clamp(v: Union[int, float], mn: Union[int, float], mx: Union[int, float]):
    return max(min(v, mx), mn)


def write_map(tilemap: dict[str, dict[str, str]], fn: str):
    with open(f"./{fn}", "w") as file:
        file.write(json.dumps(tilemap))


def type_all_in_list(l: Union[list, tuple], t: type) -> bool:
    for i in l:
        if type(i) != t:
            return False
    return True


def all_num_in_list(l: Union[list, tuple]) -> bool:
    for i in l:
        if type(i) != int and type(i) != float:
            return False
    return True
