"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
    plane.py
    cube.py - inspirado en código de ing. carlos
"""
from sphere import Materiales,Intersect
import glMatematica
from ray import *
import mmap
import numpy
import math
from cmath import pi


class Plane(object):
  def __init__(self, center, w, h, material):
    self.centro = center
    self.w = w
    self.h = h
    self.material = material

  def rays_intersection(self, orig, direction):
    d = (self.centro.y - orig.y) / direction.y
    pt = glMatematica.Resta(orig, glMatematica.Prodv3_other(direction, d))

    if d <= 0 or (self.centro.x - self.w/2) > pt.x or pt.x > (self.centro.x + self.w/2) or (self.centro.z - self.h/2) > pt.z or pt.z > (self.centro.z + self.h/2):
      return None

    normal = V3(0, 1, 0)

    return Intersect(
      distancia=d,
      point=pt,
      normales=normal
    )

class Plane_cubes(object):
  #creado para implementar cubos
  def __init__(self, center, normal, material):
    self.centro = center
    self.normal = normal
    self.material = material

  def rays_intersection(self, orig, direction):
    if glMatematica.ProdPunto( direction, self.normal) == 0:
      t = glMatematica.ProdPunto( glMatematica.Resta(self.centro, orig), self.normal)
    else:
      t = glMatematica.ProdPunto( glMatematica.Resta(self.centro, orig), self.normal) / glMatematica.ProdPunto( direction, self.normal)
    if t > 0:
      pt = glMatematica.Suma(orig, glMatematica.Prodv3_other(direction,t))

      return Intersect(
        distancia=t,
        point=pt,
        normales=self.normal
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

class cube:
  def __init__(self,center, size,material):
    self.center = center
    self.size = size
    self.material = material
    self.planos = [] #se crea el cubo utilizando planos

    mitad = (size.x/2,size.y/2,size.z/2)

    self.boundMIN = [0,0,0]
    self.boundMAX = [0,0,0]

    for i in range(3):
      #3 porque son x,y,z
        self.boundMIN[i] = self.center[i] - (0.001 + mitad[i])
        self.boundMAX[i] = self.center[i] + (0.001 + mitad[i])

    #planos que conformaran el cubo
    #lados
    self.planos.append( Plane_cubes( glMatematica.Suma_tuplaOther(center, V3(mitad[0],0,0)), V3(1,0,0), self.material ))
    self.planos.append( Plane_cubes( glMatematica.Suma_tuplaOther(center, V3(-mitad[0],0,0)), V3(-1,0,0), self.material ))

    # arriba y abajo
    self.planos.append( Plane_cubes( glMatematica.Suma_tuplaOther(center, V3(0,mitad[1],0)), V3(0,1,0), self.material ))
    self.planos.append( Plane_cubes( glMatematica.Suma_tuplaOther(center, V3(0,-mitad[1],0)), V3(0,-1,0), self.material ))

    # frente y atras
    self.planos.append( Plane_cubes( glMatematica.Suma_tuplaOther(center, V3(0,0,mitad[2])), V3(0,0,1), self.material ))
    self.planos.append( Plane_cubes( glMatematica.Suma_tuplaOther(center, V3(0,0,-mitad[2])), V3(0,0,-1), self.material ))


  def rays_intersection(self,orig,direct):
    intersect = None
    t = 99999

    for plane in self.planos:
        temp_intersect = plane.rays_intersection(orig, direct)
        if temp_intersect is not None:
            temp_point = temp_intersect.point
            if self.boundMIN[0] <= temp_point[0] <= self.boundMAX[0] and self.boundMIN[1] <= temp_point[1] <= self.boundMAX[1] and self.boundMIN[2] <= temp_point[2] <= self.boundMAX[2]:
                if temp_intersect.distancia < t:
                  t = temp_intersect.distancia
                  intersect = temp_intersect
    if intersect is None:
      return None
      
    return Intersect(
      distancia=t,
      point=intersect.point,
      normales=intersect.normales
    )