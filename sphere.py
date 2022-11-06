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

class sphere:
    #init con center, radio y color
    def  __init__(self,center, radius, clr =color(1,1,1)):
        self.center, self.radius, self.color = center,radius,clr
    
    #parametros de origen y dirección de los rays
    def rays_intersection(self, origin, direct):
        tempResta = glMatematica.Resta(self.center,origin)
        temp = (tempResta)**2 - ( glMatematica.ProdPunto( tempResta, direct) )**2

        if self.radius**2 < temp:
            #si el cuadrado del radio es menor a temp
            return None  # no es posible
        
        thc = (self.radius**2 - ( glMatematica.largoVector( glMatematica.Resta(self.center, origin) )**2 - glMatematica.ProdPunto(( glMatematica.Resta(self.center, origin) ), direct)**2 ) )**1/2
        t0 = ( (self.center - origin) * direct ) - thc
        t1 = ( (self.center - origin) * direct ) + thc

        if t0 < 0 :
            t0 = t1
        if t0 < 0:
            return None
