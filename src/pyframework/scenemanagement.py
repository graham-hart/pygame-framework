import sys
from abc import ABC

import pygame


class MainGame:
    def __init__(self, size, name: str = "Game", fps: int = 60):
        self.current_scene = None
        self.window = pygame.display.set_mode(size)
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.quit = False

    def set_scene(self, scene):
        self.current_scene = scene

    def run(self):
        while True:
            dt = self.clock.tick()
            if pygame.event.get(pygame.QUIT) or self.quit:
                self.current_scene.exit()
                sys.exit()
            self.current_scene.handle_events(pygame.event.get())
            self.current_scene.update(dt)
            self.current_scene.render(self.window)
            pygame.display.flip()

    def quit(self):
        self.quit = True


class Scene(ABC):
    def __init__(self, game: MainGame):
        self.game = game

    def handle_events(self, evts: list[pygame.event.Event]):
        pass

    def update(self, dt: int):
        pass

    def render(self, screen: pygame.Surface):
        pass
