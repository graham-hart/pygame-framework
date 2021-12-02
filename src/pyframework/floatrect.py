from __future__ import annotations

import pygame

from ptypes import Vector2


class FloatRect:
    def __init__(self, pos: Vector2, size: Vector2):
        self.pos: pygame.Vector2 = pygame.Vector2(pos)
        self.size: pygame.Vector2 = pygame.Vector2(size)

    def copy(self):
        return FloatRect((self.pos.x, self.pos.y), (self.size.x, self.size.y))

    def move(self, amount: Vector2):
        return FloatRect((self.pos.x + amount[0], self.pos.y + amount[1]), self.size)

    def move_ip(self, amount: Vector2):
        self.pos.x += amount[0]
        self.pos.y += amount[1]

    def colliderect(self, other: FloatRect):
        sbr = self.pos + self.size
        obr = other.pos + other.size
        return sbr.x >= other.pos.x and self.pos.x <= obr.x and sbr.y >= other.pos.y and self.pos.y <= obr.y

    def collidepoint(self, point: Vector2):
        return self.pos.x <= point[0] <= self.bottomright.x and self.pos.y <= point[1] <= self.bottomright.y

    def collidelistany(self, rects: list[FloatRect]):
        for rect in rects:
            if self.colliderect(rect):
                return True
        return False

    def collidelistall(self, rects: list[FloatRect]):
        for rect in rects:
            if not self.colliderect(rect):
                return False
        return True

    def update(self, pos: Vector2, size: Vector2):
        self.pos = pos
        self.size = size

    @property
    def center(self):
        return self.pos + self.size / 2

    @property
    def bottomright(self):
        return self.pos + self.size
