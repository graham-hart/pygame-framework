import json
import math
import os
from typing import Union

import pygame



class TileMap:
    def __init__(self, fn: str = None, ):
        self.chunk_size: int = 16
        # Chunks are dicts with x,y keys and
        if fn:
            self.chunks: dict[str, dict[str, str]] = read_map(fn)
        else:
            self.chunks: dict[str, dict[str, str]] = {}

    def get_chunk(self, chunk_pos: Union[pygame.Vector2, tuple[int, int]]) -> dict[str, str]:
        return self.chunks[format_map_key(chunk_pos)]

    # Get chunk containing a specific tile
    def containing_chunk_pos(self, tile_pos: Union[pygame.Vector2, tuple[int, int]]) -> pygame.Vector2:
        return pygame.Vector2(math.floor(tile_pos[0] / self.chunk_size), math.floor(tile_pos[1] / self.chunk_size))

    def get_containing_chunk(self, tile_pos: Union[pygame.Vector2, tuple[int, int]]) -> dict[str, str]:
        return self.get_chunk(self.containing_chunk_pos(tile_pos))

    # Get position of tile in chunk
    def tile_pos_in_chunk(self, tile_pos: Union[pygame.Vector2, tuple[int, int]]) -> pygame.Vector2:
        return pygame.Vector2(tile_pos[0] % self.chunk_size, tile_pos[1] % self.chunk_size)

    def tile_pos(self, chunk_pos: Union[pygame.Vector2, tuple[int, int]],
                 tile_pos: Union[pygame.Vector2, tuple[int, int]]):
        return chunk_pos[0] * self.chunk_size + tile_pos[0], chunk_pos[1] * self.chunk_size + tile_pos[1]

    # Get tile
    def get_tile(self, tile_pos: Union[pygame.Vector2, tuple[int, int]]) -> str:
        chunk = self.get_containing_chunk(tile_pos)
        tile_pos = self.tile_pos_in_chunk(tile_pos)
        return chunk[format_map_key(tile_pos)]

    # Set tile
    def set_tile(self, tile_pos: Union[pygame.Vector2, tuple[int, int]], value: str) -> None:
        chunk_pos = self.containing_chunk_pos(tile_pos)
        if chunk_pos not in self:
            self.chunks[format_map_key(chunk_pos)] = {}
        chunk = self.get_chunk(chunk_pos)
        tile_pos = self.tile_pos_in_chunk(tile_pos)
        chunk[format_map_key(tile_pos)] = value

    # If chunk is in map
    def __contains__(self, chunk_pos) -> bool:
        return format_map_key(chunk_pos) in self.chunks

    # Delete tile from map. If containing chunk is now empty, delete that chunk
    def del_tile(self, tile_pos: tuple[int, int]) -> None:
        chunk_pos = self.containing_chunk_pos(tile_pos)
        chunk = self.get_chunk(chunk_pos)
        if len(chunk) > 1:
            del chunk[format_map_key(self.tile_pos_in_chunk(tile_pos))]
        else:
            del self.chunks[format_map_key(chunk_pos)]

    def save(self, fn):
        write_map(self.chunks, fn)

    def get_visible_chunks(self, cam):
        mn, mx = cam.bounds
        chunk_min = self.containing_chunk_pos((math.floor(mn.x), math.floor(mn.y)))
        chunk_max = self.containing_chunk_pos((math.ceil(mx.x), math.ceil(mx.y)))
        chunks = {}
        for x in range(int(chunk_min.x), int(chunk_max.x)+1):
            for y in range(int(chunk_min.y), int(chunk_max.y)+1):
                if self.__contains__((x, y)):
                    chunks[format_map_key((x, y))] = self.get_chunk(
                        pygame.Vector2(x, y))
        return chunks


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


def write_map(tilemap: dict[str, dict[str, str]], fn: str):
    with open(f"./{fn}", "w") as file:
        file.write(json.dumps(tilemap))


def parse_map_key(key: str):
    return tuple(int(i) for i in key.split(","))


def format_map_key(loc: Union[tuple[int, int], pygame.Vector2]):
    return f"{int(loc[0])},{int(loc[1])}"
