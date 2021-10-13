import sys

import pygame
from pygame.locals import *

import pyframework.image
from pyframework import Camera, tilemap
from pyframework.color import Color

SIDEBAR_WIDTH = 250
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
MAP_SURF_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH

COLORS = {
    "black": Color.from_hex("#000511"),
    "darkblue": Color.from_hex("#051233"),
    "lightblue": Color.from_hex("#122a5e"),
    "darkcyan": Color.from_hex("#15526b"),
    "lightcyan": Color.from_hex("#227a7a"),
    "teal": Color.from_hex("#38ba8b"),
    "green": Color.from_hex("#55ff79"),
    "yellow": Color.from_hex("#c5ff8c"),
}

CONFIG = {
    "current_layer": 0,
    "current_tile": None,
}

PALETTE = {
}


def load_palette(path: str, cam: Camera, palette_img_size: int) -> dict[str, dict[str, object]]:
    return {
        d[0][len(path):]: {"paletteimg": pygame.transform.scale(d[1], (palette_img_size, palette_img_size)),
                           "paletterect": pygame.Rect(
                               (25, i * (palette_img_size + 10) + 30, palette_img_size, palette_img_size)),
                           "tileimg": pygame.transform.scale(d[1], (int(cam.scale.x), int(cam.scale.y)))}
        for i, d in enumerate(pyframework.image.load_paths(path).items())}


def handle_event(event):
    if event.type == QUIT:
        sys.exit()
    elif event.type == MOUSEBUTTONDOWN:
        if event.pos[0] <= SIDEBAR_WIDTH:
            for k, v in PALETTE.items():
                if v["paletterect"].collidepoint(event.pos):
                    CONFIG["current_tile"] = k
                    return


def draw_sidebar(surf):
    surf.fill(COLORS["lightcyan"].as_hex)
    for i, data in enumerate(PALETTE.items()):
        img: pygame.Surface = data[1]["paletteimg"]
        surf.blit(img, data[1]["paletterect"])
        if CONFIG["current_tile"] == data[0]:
            pygame.draw.rect(surf,COLORS["yellow"].as_hex,data[1]["paletterect"], width=4)


def draw_map(surf: pygame.Surface, cam: Camera, tm: tilemap.TileMap):
    tiles = tm.get_visible_tiles(cam)
    for coords, layers in tiles.items():
        for l in layers:
            pass


def main():
    global PALETTE
    pygame.init()

    # ----------------------------------------------------------- Camera setup
    CAM = Camera((MAP_SURF_WIDTH, SCREEN_HEIGHT), (1, 1))
    CAM.set_scale((10, 10))

    TILEMAP = tilemap.TileMap()  # Tilemap setup

    # ----------------------------------------------------------- Surfaces setup
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    MAP_SURF = pygame.Surface((MAP_SURF_WIDTH, SCREEN_HEIGHT))
    SIDEBAR_SURF = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))

    PALETTE = load_palette("mapeditor-test-imgs/", CAM, 22)

    # ----------------------------------------------------------- Timing setup
    CLOCK = pygame.time.Clock()
    dt = 1

    # ----------------------------------------------------------- Gameloop
    while True:
        dt = CLOCK.tick()
        for event in pygame.event.get():
            handle_event(event)

        MAP_SURF.fill(COLORS["darkblue"].as_hex)
        draw_map(MAP_SURF, CAM, TILEMAP)
        draw_sidebar(SIDEBAR_SURF)
        SCREEN.blit(MAP_SURF, ((SIDEBAR_WIDTH, 0), (MAP_SURF_WIDTH, SCREEN_HEIGHT)))
        SCREEN.blit(SIDEBAR_SURF, ((0, 0), (SCREEN_HEIGHT, SCREEN_HEIGHT)))
        pygame.display.flip()


if __name__ == '__main__':
    main()
