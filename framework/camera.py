import pygame as pg

import utils


class Camera:
    def __init__(self, screen_size, viewport_size):
        self.screen_width, self.screen_height = screen_size
        self.v_width, self.v_height = viewport_size
        self.x = 0
        self.y = 0
        self.scale = [self.screen_width / self.v_width, self.screen_height / self.v_height]

    def translate(self, x, y):
        if utils.all_num_in_list((x, y)):
            self.x += x
            self.y += y
        else:
            raise TypeError("Argument must be either int or float")

    def resize_viewport(self, w, h):
        if utils.all_num_in_list((w, h)):
            self.v_width, self.v_height = w, h
            self.update_scale()
        else:
            raise TypeError("Argument must be either int or float")

    def update_scale(self):
        self.scale = [self.screen_width / self.v_width, self.screen_height / self.v_height]

    def resize_window(self, w, h):
        if utils.all_num_in_list((w, h)):
            self.screen_width, self.screen_height = w, h
            self.update_scale()
        else:
            raise TypeError("Argument must be either int or float")

    # Take in screen coords and return world coords
    def unproject(self, x, y):
        if utils.all_num_in_list((x, y)):
            return x / self.scale[0] + self.x, y / self.scale[1] + self.y
        else:
            raise TypeError("Argument must be either int or float.")

    def flip_x(self):
        self.scale[0] = self.scale[0] * -1

    def flip_y(self):
        self.scale[1] = self.scale[1] * -1

    # Take in world coords and return screen coords
    def project(self, x, y):
        if utils.all_num_in_list((x, y)):
            return (x-self.x) * self.scale[0], (y - self.y) * self.scale[1]
        else:
            raise TypeError("Argument must be either int or float.")

    # Convert world distance to screen distance (above function but w/o translation)
    def project_dist(self, x, y):
        if utils.all_num_in_list((x, y)):
            return x * abs(self.scale[0]), y * abs(self.scale[1])
        else:
            raise TypeError("Argument must be either int or float.")

    # Convert screen distance to world distance (unproject function but w/o translation)
    def unproject_dist(self, x, y):
        if utils.all_num_in_list((x, y)):
            return x / abs(self.scale[0]), y / abs(self.scale[1])
        else:
            raise TypeError("Argument must be either int or float.")

    def project_rect(self, rect):
        if type(rect) == pg.Rect:
            return pg.Rect(self.project(rect.x, rect.y), self.project_dist(rect.width, rect.height))
        elif type(rect) == tuple and len(rect) == 2 and utils.type_all_in_list(rect, tuple) and utils.all_num_in_list(
                list(rect[0]) + list(rect[1])):
            return self.project(rect[0][0], rect[0][1]), self.project_dist(rect[1][0], rect[1][1])
        elif type(rect) == tuple and len(rect) == 4 and utils.all_num_in_list(rect):
            return *self.project(rect[0], rect[1]), *self.project_dist(rect[2], rect[3])
        else:
            raise TypeError("Argument must be rect-style object.")

    def unproject_rect(self, rect):
        if type(rect) == pg.Rect:
            return pg.Rect(self.unproject(rect.x, rect.y), self.unproject_dist(rect.width, rect.height))
        elif type(rect) == tuple and len(rect) == 2 and utils.type_all_in_list(rect, tuple) and utils.type_all_in_list(rect[0],
                                                                                                                       int) and utils.type_all_in_list(
            rect[1], int):
            return self.unproject(rect[0][0], rect[0][1]), self.unproject_dist(rect[1][0], rect[1][1])
        elif type(rect) == tuple and len(rect) == 4 and utils.type_all_in_list(rect, int):
            return *self.unproject(rect[0], rect[1]), *self.unproject_dist(rect[2], rect[3])
        else:
            raise TypeError("Argument must be rect-style object.")
