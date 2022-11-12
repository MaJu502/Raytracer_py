"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
    sphere.py
"""
from ray import *
import glMatematica

def color(r,g,b):
    # number between 0 and 255 for each input
    r = int(r *255)
    g = int(g *255)
    b = int(b *255)
    return bytes([b, g, r])
    

class Light(object):
    def __init__(self, posicion=V3(0,0,0), intensity=1):
        self.position = posicion
        self.intensity = intensity

class Materiales(object):
    def __init__(self, diff=color(1,1,1), albedo=(1, 0), spec=0):
        self.diffuse = diff
        self.albedo = albedo
        self.spec = spec

class Intersect(object):
  def __init__(self, distancia, point, normales):
    self.distancia = distancia
    self.point = point
    self.normales = normales

class sphere:
    #init con center, radio y color
    def  __init__(self,center, radius, material):
        self.center, self.radius, self.material = center,radius,material
    
    #parametros de origen y dirección de los rays
    def rays_intersection(self, origin, direct):
        tempResta = glMatematica.Resta(self.center,origin)
        temp = (glMatematica.largoVector(tempResta))**2 - ( glMatematica.ProdPunto( tempResta, direct) )**2

        if temp > self.radius**2:
            
            #si el cuadrado del radio es menor a temp
            return None  # no es posible
        
        thc = (self.radius**2 - ( glMatematica.largoVector( glMatematica.Resta(self.center, origin) )**2 - glMatematica.ProdPunto(( glMatematica.Resta(self.center, origin) ), direct)**2 ) )**1/2
        t0 = glMatematica.ProdPunto( (glMatematica.Resta(self.center,origin)),direct ) - thc
        t1 = glMatematica.ProdPunto( (glMatematica.Resta(self.center,origin)),direct ) + thc

        if t0 < 0 or t1 < 1:
            return None
        
        temp_hit = glMatematica.Suma(origin, glMatematica.ProdPunto( direct, t0 ))
        norm = glMatematica.Normalizar( glMatematica.Resta( temp_hit, self.center ) )
        #ahora se devuelven distancia, punto y normal
        return Intersect( distancia=t0, point=temp_hit,normales=norm)
