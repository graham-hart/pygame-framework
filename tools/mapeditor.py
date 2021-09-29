import sys

import pygame
from pygame.locals import *

from package import pyframework as f

SIDEBAR_WIDTH = 250
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
MAP_SURF_WIDTH = SCREEN_WIDTH - SIDEBAR_WIDTH

COLORS = {
    "black": f.Color.from_hex("#000511"),
    "darkblue": f.Color.from_hex("#051233"),
    "lightblue": f.Color.from_hex("#122a5e"),
    "darkcyan": f.Color.from_hex("#15526b"),
    "lighcyan": f.Color.from_hex("#227a7a"),
    "teal": f.Color.from_hex("#38ba8b"),
    "green": f.Color.from_hex("#55ff79"),
    "yellow": f.Color.from_hex("#c5ff8c"),
}


def draw_sidebar(surf):
    pass


def draw_map(surf, cam, tilemap):
    pass


def main():
    pygame.init()

    # ----------------------------------------------------------- Camera setup
    CAM = f.Camera((MAP_SURF_WIDTH, SCREEN_HEIGHT), (1, 1))
    CAM.set_scale((10, 10))

    # ----------------------------------------------------------- Tilemap setup
    TILEMAP = f.tilemap.TileMap()

    # ----------------------------------------------------------- Surfaces setup
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    MAP_SURF = pygame.Surface((MAP_SURF_WIDTH, SCREEN_HEIGHT))
    SIDEBAR_SURF = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))

    # ----------------------------------------------------------- Timing setup
    CLOCK = pygame.time.Clock()
    dt = 0.1

    # ----------------------------------------------------------- Gameloop
    while True:
        dt = CLOCK.tick()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
        SIDEBAR_SURF.fill(COLORS["teal"].as_hex)
        SCREEN.blit(MAP_SURF, ((SIDEBAR_WIDTH, 0), (MAP_SURF_WIDTH, SCREEN_HEIGHT)))
        SCREEN.blit(SIDEBAR_SURF, ((0, 0), (SCREEN_HEIGHT, SCREEN_HEIGHT)))
        pygame.display.flip()


if __name__ == '__main__':
    main()
