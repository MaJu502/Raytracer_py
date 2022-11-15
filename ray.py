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


class Raytracer:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        self.background_color = Black
        self.current_color = White

        self.pixels = []
        self.items = []
        self.light = None
        self.enviroment_map = None

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
    
    def background(self,direct):
        #para revisar si tiene envmap
        if self.envmap:
            return self.envmap.get_color(direct)
        return self.background_color

    def rtRender(self):
        temp_fov = int(pi * 1/2)
        for y in range(self.height):
            for x in range(self.width):
                i = ((2 * (x + 0.5) / self.width) - 1) * tan(temp_fov/2) * (self.width/self.height)
                j = (1 - (2 * (y + 0.5) / self.width)) * tan(temp_fov/2)
                direction = glMatematica.Normalizar(V3(i,j,-1))
                temp_clr = self.cast_ray(V3(0, 0, 0), direction)
                self.glVertex(x, y, temp_clr)

    def inteseccion(self, orig, direct):
        zBuffed = 99999 #simulando float('inf')
        mat, inter = None,None

        for x in self.items:
            temp_hit = x.rays_intersection(orig,direct)
            if temp_hit and temp_hit.distancia < zBuffed:
                #si existe una interseccion y es menor al buffer
                zBuffed = temp_hit.distancia
                mat = x.material
                inter = temp_hit
        return mat,inter

    def cast_ray(self, origin, direction,recursiones=0):
        material, intersect = self.inteseccion(origin, direction)
        
        if material is None or recursiones >= 3:
            if self.enviroment_map:
                return self.enviroment_map
            return self.background_color
        offset = glMatematica.Prodv3_other(intersect.normales, 1.1)

        if material.albedo[2] > 0:
            reverse_dir = glMatematica.Prodv3_other(direction,-1)
            reflect_dir = glMatematica.reflect(reverse_dir, intersect.normales)
            if glMatematica.ProdPunto(reflect_dir, intersect.normales) < 0:
                reflect_orig = glMatematica.Resta( intersect.point, offset )
            else: 
                reflect_orig = glMatematica.Suma( intersect.point, offset )
            reflect_color = self.cast_ray( reflect_orig, reflect_dir, recursiones +1 )
        else: 
            reflect_color = color(0,0,0)
        
        final_reflection_r = int(reflect_color[2] * material.albedo[2])
        final_reflection_g = int(reflect_color[1] * material.albedo[2])
        final_reflection_b = int(reflect_color[0] * material.albedo[2])


        if material.albedo[3] > 0:
            refract_dir = glMatematica.refract(direction, intersect.normales, material.refractive_index)
            if glMatematica.ProdPunto(refract_dir, intersect.normales) < 0:
                refract_orig = glMatematica.Resta(intersect.point, offset)
            else:
                 glMatematica.Suma(intersect.point, offset)

            refract_color = self.cast_ray(refract_orig, refract_dir, recursiones + 1)
        else:
            refract_color = color(0, 0, 0)

        final_refraction_r = int(refract_color[2] * material.albedo[3])
        final_refraction_g = int(refract_color[1] * material.albedo[3])
        final_refraction_b = int(refract_color[0] * material.albedo[3])
        

        light_dir = glMatematica.Normalizar(glMatematica.Resta(self.light.position, intersect.point))
        light_dist = glMatematica.largoVector( glMatematica.Resta(self.light.position, intersect.point) )

        #hay que definir las intensidades respecto a las sombras
        if glMatematica.ProdPunto( light_dir, intersect.normales) < 0:
            s_orig = glMatematica.Resta(intersect.point, offset)
        else:
            s_orig = glMatematica.Suma(intersect.point, offset)

        s_mat, s_inter = self.inteseccion( s_orig, light_dir )
        s_intensity = 0 #default que puede cambiar a continuacion
        if s_inter and s_mat:
            if glMatematica.largoVector(glMatematica.Resta(s_inter.point, s_orig)) < light_dist:
                s_intensity = 0.6 #puede cambiar el valor segun se requiera la escena
        
        temp_intensidad = self.light.intensity * max(0, glMatematica.ProdPunto(light_dir, intersect.normales)) * (1 - s_intensity)
        
        # Diffuse component
        #diffuse_intensity = glMatematica.ProdPunto(light_dir, intersect.normales)
        diffuse_0 = int(material.diffuse[2] * temp_intensidad * material.albedo[0])
        diffuse_1 = int(material.diffuse[1] * temp_intensidad * material.albedo[0])
        diffuse_2 = int(material.diffuse[0] * temp_intensidad * material.albedo[0])
       
        # Specular component
        light_reflection = glMatematica.reflect(light_dir, intersect.normales)
        reflection_intensity = max(0, glMatematica.ProdPunto(light_reflection, direction))
        specular_intensity = self.light.intensity * (reflection_intensity ** material.spec)
        specular_0 = int(self.light.colores[2] * specular_intensity * material.albedo[1])
        specular_1 = int(self.light.colores[1] * specular_intensity * material.albedo[1])
        specular_2 = int(self.light.colores[0] * specular_intensity * material.albedo[1])

        #ahora tengo que armar el color que se retorna
        r = diffuse_0 + specular_0 + final_refraction_r + final_reflection_r
        g = diffuse_1 + specular_1 + final_refraction_g + final_reflection_g
        b = diffuse_2 + specular_2 + final_refraction_b + final_reflection_b

        return color(r/255,g/255,b/255)

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
