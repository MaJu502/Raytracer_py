"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""

from collections import namedtuple
from math import pi, tan
import struct
import glMatematica
from sphere import *
from vectors import *

# char, word, double word #
def ch(x):
    return struct.pack('=c',x.encode('ascii'))
def wrd(x):
    return struct.pack('=h', x)
def dwrd(x):
    return struct.pack('=l', x)

# colors #
def color(r,g,b):
    # number between 0 and 255 for each input
    r = int(r *255)
    g = int(g *255)
    b = int(b *255)
    return bytes([b, g, r])

Black = color(0,0,0)
White = color(1,1,1)

def coordenadasbaricentricas(A,B,C,k):
    lasbaricentricas = glMatematica.ProdCruz(
        V3(C.x - A.x, B.x - A.x, A.x - k.x), 
        V3(C.y - A.y, B.y - A.y, A.y - k.y)
    )

    if abs(lasbaricentricas[2]) < 1:
        return -1, -1, -1

    return (
        1 - (lasbaricentricas[0] + lasbaricentricas[1]) / lasbaricentricas[2], 
        lasbaricentricas[1] / lasbaricentricas[2], 
        lasbaricentricas[0] / lasbaricentricas[2]
    )

#change
def allbarycentric(A, B, C, bbox_min, bbox_max):
  barytransform = numpy.linalg.inv([[A.x, B.x, C.x], [A.y,B.y,C.y], [1, 1, 1]])
  grid = numpy.mgrid[bbox_min.x:bbox_max.x, bbox_min.y:bbox_max.y].reshape(2,-1)
  grid = numpy.vstack((grid, numpy.ones((1, grid.shape[1]))))
  barycoords = numpy.dot(barytransform, grid)
  # barycoords = barycoords[:,numpy.all(barycoords>=0, axis=0)]
  barycoords = numpy.transpose(barycoords)
  return barycoords


class Raytracer:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.background_color = Black
        self.current_color = White

        self.pixels = []
        self.items = []
        self.glClear()

    def glClear(self):
        self.pixels = [
            [self.background_color for x in range (self.width)] for y in range (self.height)
        ]

    def glVertex(self, ingx, ingy, optColor=None):
        try:
            self.pixels[ingy][ingx] = optColor or self.curr_color
        except:
        # To avoid index out of range exceptions
            pass

    def rtRender(self):
        temp_fov = int(pi * 1/2)
        for y in range(self.height):
            for x in range(self.width):
                i = ((2 * (x + 0.5) / self.width) - 1) * tan(temp_fov/2) * (self.width/self.height)
                j = (1 - (2 * (y + 0.5) / self.width)) * tan(temp_fov/2)
                direction = glMatematica.Normalizar(V3(i,j,-1))
                temp_clr = self.cast_ray(V3(0, 0, 0), direction)
                self.glVertex(x, y, temp_clr)

    def cast_ray(self,orig, direction):
        for x in self.items:
            #por cada item que se tenga que renderizar
            if x.rays_intersection(orig,direction):
                #si devuelve true
                retorno_clr = x.color #cambia el color de la esfera

        return retorno_clr

    def glFinish(self,filename):
        op = open(filename, 'bw')

        #Header
        op.write(ch('B'))
        op.write(ch('M'))
        op.write(dwrd( 14 + 40 + (self.width * self.height * 3)))
        op.write(dwrd(0))
        op.write(dwrd(14 + 40))

        #Image
        op.write(dwrd(40))
        op.write(dwrd(self.width))
        op.write(dwrd(self.height))
        op.write(wrd(1))
        op.write(wrd(24))
        op.write(dwrd(0))
        op.write(dwrd(self.width * self.height * 3)) #screen size
        op.write(dwrd(0))
        op.write(dwrd(0))
        op.write(dwrd(0))
        op.write(dwrd(0))

        #Color/Pixel data
        for x in range(self.height):
            for y in range(self.width):
                op.write(self.pixels[x][y])
        op.close()
