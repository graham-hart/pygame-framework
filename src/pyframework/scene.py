import sys
from abc import ABC

import pygame
from typing import Type


class MainGame:
    def __init__(self, size, name: str = "Game", fps: int = 60, flags: list = []):
        self.current_scene = None
        self.window = pygame.display.set_mode(size, *flags)
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.quit_flag = False

    def set_scene(self, scenetype: Type, *args, **kwargs):
        if issubclass(scenetype, Scene):
            self.current_scene = scenetype(self,*args, **kwargs)
        else:
            raise TypeError("Argument 'scene' must be a subclass of type Scene")

    def run(self):
        while True:
            dt = self.clock.tick()
            if pygame.event.get(pygame.QUIT) or self.quit_flag:
                self.current_scene.exit()
                sys.exit()
            self.current_scene.handle_events(pygame.event.get())
            self.current_scene.update(dt)
            self.current_scene.render(self.window)
            pygame.display.flip()

    def quit(self):
        self.quit_flag = True

    def screen_width(self):
        return self.window.get_width()

    def screen_height(self):
        return self.window.get_width()

    def screen_size(self):
        return self.window.get_size()


class Scene(ABC):
    def __init__(self, game):
        if issubclass(type(game), MainGame):
            self.game = game
        else:
            raise TypeError("Argument 'game' must be a subclass of type MainGame")

    def handle_events(self, evts: list[pygame.event.Event]):
        raise NotImplementedError

    def update(self, dt: int):
        raise NotImplementedError

    def render(self, screen: pygame.Surface):
        raise NotImplementedError

    def exit(self):
        raise NotImplementedError
