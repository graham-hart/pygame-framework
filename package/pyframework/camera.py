from typing import Union

import pygame

class Camera:
    # TODO: 0,0 should be at center
    def __init__(self, screen_size, viewport_size):
        self.v_size: pygame.Vector2 = pygame.Vector2(viewport_size)
        self.sc_size: pygame.Vector2 = pygame.Vector2(screen_size)
        self.pos: pygame.Vector2 = pygame.Vector2(0, 0)
        self.scale: pygame.Vector2 = pygame.Vector2()
        self._update_scale()

    def project_x(self, x: Union[int, float]):
        return (x - self.pos.x + self.center.x) * self.scale.x

    def project_y(self, y: Union[int, float]):
        return (y - self.pos.y + self.center.y) * self.scale.y

    def unproject_x(self, x: Union[int, float]):
        return x / self.scale.x + self.pos.x - self.center.x

    def unproject_y(self, y: Union[int, float]):
        return y / self.scale.y + self.pos.y - self.center.y

    def project_x_dist(self, x: Union[int, float]):
        return x * self.scale.x

    def project_y_dist(self, y: Union[int, float]):
        return y * self.scale.y

    def unproject_x_dist(self, x: Union[int, float]):
        return x / self.scale.x

    def unproject_y_dist(self, y: Union[int, float]):
        return y / self.scale.y

    def project(self, pos: Union[tuple[int, int], tuple[float, float]]) -> tuple:
        return self.project_x(pos[0]), self.project_y(pos[1])

    def unproject(self, pos: Union[tuple[int, int], tuple[float, float]]) -> tuple:
        return self.unproject_x(pos[0]), self.unproject_y(pos[1])

    def project_dist(self, size: Union[tuple[int, int], tuple[float, float], pygame.Vector2]) -> tuple:
        return self.project_x_dist(size[0]), self.project_y_dist(size[1])

    def unproject_dist(self, size: Union[tuple[int, int], tuple[float, float], pygame.Vector2]) -> tuple:
        return self.unproject_x_dist(size[0]), self.unproject_y_dist(size[1])

    def project_rect(self,
                     rect: Union[tuple[int, int, int, int], tuple[float, float, float, float], tuple[
                         tuple[int, int], tuple[int, int]], tuple[
                                     tuple[float, float], tuple[float, float]], pygame.Rect]):
        if len(rect) == 4 and type(rect) == tuple:
            return *self.project((rect[0], rect[1])), *self.project_dist((rect[2], rect[3]))
        elif len(rect) == 2:
            return self.project(rect[0]), self.project_dist(rect[1])
        elif type(rect) == pygame.Rect:
            return pygame.Rect((self.project_x(rect.x), self.project_y(rect.y), self.project_x_dist(rect.width),
                                self.project_y_dist(rect.height)))

    def unproject_rect(self,
                       rect: Union[tuple[int, int, int, int], tuple[float, float, float, float], tuple[
                           tuple[int, int], tuple[int, int]], tuple[
                                       tuple[float, float], tuple[float, float]], pygame.Rect]):
        if len(rect) == 4 and type(rect) == tuple:
            return *self.unproject((rect[0], rect[1])), *self.unproject_dist((rect[2], rect[3]))
        elif len(rect) == 2:
            return self.unproject(rect[0]), self.unproject_dist(rect[1])
        elif type(rect) == pygame.Rect:
            return pygame.Rect((self.unproject_x(rect.x), self.unproject_y(rect.y), self.unproject_x_dist(rect.width),
                                self.unproject_y_dist(rect.height)))

    def translate(self, pos: Union[tuple[int, int], tuple[float, float], pygame.Vector2]):
        self.pos += pos

    def set_scale(self, scale: Union[tuple[int, int], tuple[float, float], pygame.Vector2]):
        if type(scale) is tuple:
            self.scale.update(scale)
        else:
            self.scale = scale
        self.v_size.update(self.sc_size.x / self.scale.x, self.sc_size.y / self.scale.y)

    def _update_scale(self):
        self.scale.update(self.sc_size.x / self.v_size.x, self.sc_size.y / self.v_size.y)

    def resize_viewport(self, size: Union[tuple[int, int], pygame.Vector2]):
        if type(size) is tuple:
            self.v_size.update(size)
        else:
            self.v_size = size
        self._update_scale()

    def resize_screen(self, size: Union[tuple[int, int], pygame.Vector2]):
        if type(size) is tuple:
            self.sc_size.update(size)
        else:
            self.sc_size = size
        self._update_scale()

    @property
    def bounds(self):
        return pygame.Vector2(self.pos.x - self.center.x, self.pos.y - self.center.y), pygame.Vector2(
            self.pos.x + self.center.x, self.pos.y + self.center.y)

    @property
    def center(self):
        return self.v_size/2
