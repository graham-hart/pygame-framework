import colorsys
import random

from . import utils


class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.r = utils.clamp(r, 0, 255)
        self.g = utils.clamp(g, 0, 255)
        self.b = utils.clamp(b, 0, 255)
        self.a = utils.clamp(a, 0, 255)

    @property
    def as_hex(self):
        return ('#%02x%02x%02x' % (self.r, self.g, self.b)) if self.a == 255 else '#%02x%02x%02x%02x' % (
            self.r, self.g, self.b, self.a)

    @property
    def as_hsv(self):
        c = colorsys.rgb_to_hsv(self.r / 255, self.g / 255, self.b / 255)
        return round(c[0] * 360), round(c[1] * 255), round(c[2] * 255)

    @property
    def as_tuple(self):
        if self.a == 255:
            return self.r, self.g, self.b
        return self.r, self.g, self.b, self.a

    def __repr__(self):
        s = f"[{self.r}, {self.g}, {self.b}"
        return s + f", {self.a}]" if self.a != 255 else s + "]"

    def __add__(self, other):
        if type(other) is Color:
            return Color(self.r + other.r, self.g + other.g, self.b + other.b, self.a + other.a)
        elif type(other) is tuple:
            return Color(self.r + other[0], self.g + other[1], self.b + other[2], self.a + other[3])

    def __sub__(self, other):
        if type(other) is Color:
            return Color(self.r - other.r, self.g - other.g, self.b - other.b, self.a - other.a)
        elif type(other) is tuple:
            return Color(self.r - other[0], self.g - other[1], self.b - other[2], self.a - other[3])

    @staticmethod
    def random_rgb():
        return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def from_hsv(h, s, v):
        c = colorsys.hsv_to_rgb(h / 360, s / 255, v / 255)
        print(c)
        return Color(round(c[0] * 255), round(c[1] * 255), round(c[2] * 255))

    @staticmethod
    def from_hex(h: str):
        h = h.strip("#")
        if len(h) == 6:
            return Color(int(h[:2], 16), int(h[2:4], 16), int(h[4:], 16))
        elif len(h) == 8:
            return Color(int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:]))
        else:
            raise ValueError("Hex string must be 7 or 9 characters long (including '#')")


def color_lerp(color1: Color, color2: Color, amt: float):
    if not (0 <= amt <= 1):
        raise ValueError("Amount must be a decimal between 0 and 1")
    diff = (color2.r - color1.r) * amt, (color2.g - color1.g) * amt, (color2.b - color1.b) * amt, (
            color2.a - color1.a) * amt
    return color1 + diff
