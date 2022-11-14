"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
    plane.py
"""
from sphere import Materiales,Intersect
import glMatematica
from ray import *

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
