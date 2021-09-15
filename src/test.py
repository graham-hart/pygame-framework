import sys

import pygame
from pygame.locals import *

from framework.camera import Camera


def main():
    pygame.init()
    SC_SIZE = WIDTH, HEIGHT = 500, 500
    W_SIZE = W_W, W_H = 10, 10
    cam = Camera(SC_SIZE, W_SIZE)
    cam.set_pos(-cam.v_width / 2, -cam.v_height / 2)
    sc = pygame.display.set_mode(SC_SIZE)
    pygame.display.set_caption("Framework")
    while 1:
        for evt in pygame.event.get():
            if evt.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        print(cam.project(0, 0))
        pygame.draw.circle(sc, (255, 255, 255), cam.project(0, 0), 30)
        pygame.display.flip()
    print("Bye!")


if __name__ == "__main__":
    main()
