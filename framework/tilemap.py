import math

from framework import utils


class TileMap:
    def __init__(self, chunk_size: int, fn: str = None, ):
        self.chunk_size: int = chunk_size
        # Chunks are dicts with x,y keys and
        if fn:
            self.chunks: dict[str, dict[str, str]] = utils.read_map(fn)
        else:
            self.chunks: dict[str, dict[str, str]] = {}

    def get_chunk(self, chunk_pos: tuple[int, int]) -> dict[str, str]:
        return self.chunks[utils.format_map_key(chunk_pos)]

    # Get chunk containing a specific tile
    def containing_chunk_pos(self, tile_pos: tuple[int, int]) -> tuple[int, int]:
        return math.floor(tile_pos[0] / self.chunk_size), math.floor(tile_pos[1] / self.chunk_size)

    def get_containing_chunk(self, tile_pos: tuple[int, int]) -> dict[str, str]:
        return self.get_chunk(self.containing_chunk_pos(tile_pos))

    # Get position of tile in chunk
    def tile_pos_in_chunk(self, tile_pos: tuple[int, int]) -> tuple[int, int]:
        return tile_pos[0] % self.chunk_size, tile_pos[1] % self.chunk_size

    # Get tile
    def get_tile(self, tile_pos: tuple[int, int]) -> str:
        chunk = self.get_containing_chunk(tile_pos)
        tile_pos = self.tile_pos_in_chunk(tile_pos)
        return chunk[utils.format_map_key(tile_pos)]

    # Set tile
    def set_tile(self, tile_pos: tuple[int, int], value: str) -> None:
        chunk_pos = self.containing_chunk_pos(tile_pos)
        if chunk_pos not in self:
            self.chunks[utils.format_map_key(chunk_pos)] = {}
        chunk = self.get_chunk(chunk_pos)
        tile_pos = self.tile_pos_in_chunk(tile_pos)
        chunk[utils.format_map_key(tile_pos)] = value

    # If chunk is in map
    def __contains__(self, chunk_pos) -> bool:
        return utils.format_map_key(chunk_pos) in self.chunks

    # Delete tile from map. If containing chunk is now empty, delete that chunk
    def del_tile(self, tile_pos: tuple[int, int]) -> None:
        chunk_pos = self.containing_chunk_pos(tile_pos)
        chunk = self.get_chunk(chunk_pos)
        if len(chunk) > 1:
            del chunk[utils.format_map_key(self.tile_pos_in_chunk(tile_pos))]
        else:
            del self.chunks[utils.format_map_key(chunk_pos)]

    def save(self, fn):
        utils.write_map(self.chunks, fn)
