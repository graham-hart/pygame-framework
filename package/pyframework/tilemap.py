import json
import math
import os
from typing import Union

import pygame


class TileMap:
    def __init__(self, dct=None):
        self.tiles = dct if dct else {}

    def tuplify(self):
        tmp = {}
        for i, v in self.tiles.items():
            tmp[parse_map_key(i)] = v
        self.tiles = tmp

    def stringify(self):
        tmp = {}
        for i, v in self.tiles.items():
            tmp[format_map_key(i)] = v

    def get_tile(self, tile_pos: Union[pygame.Vector2, tuple[int, int]]):
        return self.tiles[tile_pos[0],tile_pos[1]]

    # Set tile
    def set_tile(self, tile_pos: Union[pygame.Vector2, tuple[int, int]], value: str) -> None:
        self.tiles[tile_pos[0], tile_pos[1]] = value

    # If chunk is in map
    def __contains__(self, tile_pos: Union[pygame.Vector2, tuple[int, int]]) -> bool:
        return (tile_pos[0], tile_pos[1]) in self.tiles

    # Delete tile from map. If containing chunk is now empty, delete that chunk
    def del_tile(self, tile_pos: Union[pygame.Vector2, tuple[int, int]]) -> None:
        del self.tiles[tile_pos[0], tile_pos[1]]

    def get_visible_tiles(self, cam):
        mn, mx = cam.bounds
        chunks = {}
        for x in range(int(mn.x), int(mx.x) + 1):
            for y in range(int(mn.y), int(mx.y) + 1):
                if self.__contains__((x, y)):
                    chunks[format_map_key((x, y))] = self.get_tile((x,y))
        return chunks

    @staticmethod
    def load_map(fn: str):
        if os.path.exists(fn):
            with open(fn, "r+") as file:
                data = json.loads(file.read())
                t = TileMap(data)
                t.tuplify()
        else:
            raise FileNotFoundError(f"Path '{fn}' not found")

    def save(self, fn: str):
        self.tuplify()
        with open(fn, "w+") as file:
            file.write((json.dumps(self.dict)))



def parse_map_key(key: str):
    return tuple(int(i) for i in key.split(","))


def format_map_key(loc: Union[tuple[int, int], pygame.Vector2]):
    return f"{int(loc[0])},{int(loc[1])}"
