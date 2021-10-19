import json
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

    # Get all layers at x,y
    def get_slice(self, tile_pos: Union[pygame.Vector2, tuple[int, int]]) -> dict[int, str]:
        return self.tiles[tile_pos[0], tile_pos[1]]

    # Get tiles at x,y,z
    def get_tile(self, tile_pos: Union[pygame.Vector3, tuple[int, int, int]]) -> str:
        return self.tiles[tile_pos[0], tile_pos[1]][tile_pos[2]]

    # Set tile
    def set_tile(self, tile_pos: Union[pygame.Vector3, tuple[int, int, int]], value: str) -> None:
        if (tile_pos[0], tile_pos[1]) not in self.tiles:
            self.tiles[tile_pos[0], tile_pos[1]] = {}
        self.tiles[tile_pos[0], tile_pos[1]][tile_pos[2]] = value

    # Delete tile from map
    def del_tile(self, tile_pos: Union[pygame.Vector3, tuple[int, int, int]]) -> None:
        if len(self.tiles[tile_pos[0], tile_pos[1]]) == 1:
            del self.tiles[tile_pos[0], tile_pos[1]]
        else:
            del self.tiles[tile_pos[0], tile_pos[1]][tile_pos[2]]

    def get_visible_tiles(self, cam):
        mn, mx = cam.bounds
        tiles = {}
        for x in range(int(mn.x-1), int(mx.x+1)):
            for y in range(int(mn.y-1), int(mx.y+1)):
                if (x, y) in self.tiles:
                    tiles[x, y] = self.get_slice((x, y))
        return tiles

    def has_tile(self, pos: tuple[int,int,int]):
        if (pos[0],pos[1]) in self.tiles:
            return pos[2] in self.tiles[pos[0], pos[1]]
        return False

    @staticmethod
    def load_map(fn: str):
        if os.path.exists(fn):
            with open(fn, "r+") as file:
                data = json.loads(file.read())
                t = TileMap(data)
                t.tuplify()
                return t
        else:
            raise FileNotFoundError(f"Path '{fn}' not found")

    def save(self, fn: str):
        self.stringify()
        with open(fn, "w+") as file:
            file.write((json.dumps(self.tiles)))


def parse_map_key(key: str):
    return tuple(int(i) for i in key.split(","))


def format_map_key(loc: Union[tuple[int, int], pygame.Vector2]):
    return f"{int(loc[0])},{int(loc[1])}"
