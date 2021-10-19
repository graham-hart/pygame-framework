import math
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
    "current_tile": "",
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
            pygame.draw.rect(surf, COLORS["yellow"].as_hex, data[1]["paletterect"], width=4)


def draw_map(surf: pygame.Surface, cam: Camera, tm: tilemap.TileMap):
    surf.fill(COLORS["darkblue"].as_hex)
    tiles = tm.get_visible_tiles(cam)
    for coords, layers in tiles.items():
        for l in layers.values():
            surf.blit(PALETTE[l]["tileimg"], PALETTE[l]["tileimg"].get_rect().move(cam.project(coords)))


def edit_map(tm: tilemap.TileMap, cam: Camera):
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos[0] > SIDEBAR_WIDTH:
        mouse_state = pygame.mouse.get_pressed(3)
        tmp: tuple[float, float] = cam.unproject((mouse_pos[0] - SIDEBAR_WIDTH, mouse_pos[1]))
        world_mouse_pos: tuple[int, int, int] = math.floor(tmp[0]), math.floor(tmp[1]), CONFIG["current_layer"]
        if mouse_state[0] and CONFIG["current_tile"] != "" and world_mouse_pos[0]:
            tm.set_tile(world_mouse_pos, CONFIG["current_tile"])
        elif mouse_state[2]:
            if tm.has_tile(world_mouse_pos):
                tm.del_tile(world_mouse_pos)


def move(cam: Camera, dt):
    keys = pygame.key.get_pressed()
    t: list[int] = [0, 0]
    move_speed = 1 * dt
    if keys[K_w]:
        t[1] -= move_speed
    if keys[K_s]:
        t[1] += move_speed
    if keys[K_a]:
        t[0] -= move_speed
    if keys[K_d]:
        t[0] += move_speed
    cam.translate((t[0], t[1]))


def main():
    global PALETTE
    pygame.init()

    # ----------------------------------------------------------- Surfaces setup
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Map Editor")
    MAP_SURF = pygame.Surface((MAP_SURF_WIDTH, SCREEN_HEIGHT))
    SIDEBAR_SURF = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))

    # ----------------------------------------------------------- Camera setup
    CAM = Camera((MAP_SURF_WIDTH, SCREEN_HEIGHT), (1, 1))
    CAM.set_scale((20, 20))

    TILEMAP = tilemap.TileMap()  # Tilemap setup

    PALETTE = load_palette("mapeditor-test-imgs/", CAM, 22)

    # ----------------------------------------------------------- Timing setup
    CLOCK = pygame.time.Clock()
    dt = 1

    # ----------------------------------------------------------- Gameloop
    while True:
        dt = CLOCK.tick() / 60
        for event in pygame.event.get():
            handle_event(event)
        edit_map(TILEMAP, CAM)
        draw_map(MAP_SURF, CAM, TILEMAP)
        draw_sidebar(SIDEBAR_SURF)
        move(CAM, dt)
        SCREEN.blit(MAP_SURF, ((SIDEBAR_WIDTH, 0), (MAP_SURF_WIDTH, SCREEN_HEIGHT)))
        SCREEN.blit(SIDEBAR_SURF, ((0, 0), (SCREEN_HEIGHT, SCREEN_HEIGHT)))
        pygame.display.flip()


if __name__ == '__main__':
    main()
