"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""
from re import X
import struct

def color(r, g, b):
    return bytes([b, g, r])

# texturas #
class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        # se lee el documento 
        image = open(self.path, "rb")
        image.seek(2 + 4 + 4)
        header_size = struct.unpack("=l", image.read(4))[0]
        image.seek(2 + 4 + 4 + 4 + 4)
        self.width = struct.unpack("=l", image.read(4))[0]
        self.height = struct.unpack("=l", image.read(4))[0]
        image.seek(header_size)

        self.pixels = [] #donde se guardaran los pixeles

        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))

                self.pixels[y].append(color(r,g,b))

        image.close()

    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)

        # return self.pixels[y][x]
        try:
            b = round(self.pixels[y][x][0] * intensity)
            g = round(self.pixels[y][x][1] * intensity)
            r = round(self.pixels[y][x][2] * intensity)
        except:
            b = 255 * intensity
            g = 255 * intensity
            r = 255 * intensity

        return color(r,g,b)