import colorsys
import random


class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

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
            return Color(int(h[:2], 16), int(h[2:4], 16), int(h[4:],16))
        elif len(h) == 8:
            return Color(int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:]))
        else:
            raise ValueError("Hex string must be 7 or 9 characters long (including '#')")

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
