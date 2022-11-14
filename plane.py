"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
    plane.py
"""
from sphere import Materiales,Intersect
import glMatematica
from ray import *
import mmap
import numpy
import math
from cmath import pi


class Plane(object):
  def __init__(self, y, material):
    self.y = y
    self.material = material

  def rays_intersection(self, orig, direction):
    d = -(orig.y + self.y) / direction.y
    pt = glMatematica.Suma(orig, glMatematica.Prodv3_other(direction, d))

    if d <= 0 or abs(pt.x) > 2 or pt.z > -5 or pt.z < -10:
      return None

    normal = V3(0, 1, 0)

    return Intersect(
      distance=d,
      point=pt,
      normal=normal
    )


class envmap:
  def __init__(self, path) -> None:
    self.path = path
    self.read()

  def read(self):
    imagen = open(self.path, 'rb')
    m = mmap.mmap(imagen.fileno(), 0, access=mmap.ACCESS_READ)
    ba = bytearray(m)
    header_size = struct.unpack("=l", ba[10:14])[0]
    self.width = struct.unpack("=l", ba[18:22])[0]
    self.height = struct.unpack("=l", ba[18:22])[0]
    all_bytes = ba[header_size::]
    self.pixels = numpy.frombuffer(all_bytes, dtype='uint8')
    imagen.close()

  def get_color(self, direction):
    direction = glMatematica.Normalizar(direction)
    x = int((math.atan2(direction.z, direction.x) / (2 * pi) + 0.5) * self.width)
    y = int(math.acos(-direction.y) / pi * self.height)
    index = (y * self.width + x) * 3 % len(self.pixels)

    processed = self.pixels[index:index+3].astype(numpy.uint8)
    return color(processed[2], processed[1], processed[0])