"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
se usan valores de 0 a 1 para los colores en esta version
"""
from ray import *
from sphere import *
from vectors import *
from plane import *

rt = Raytracer(700,700)
rt.glClear()

#materiales para osos 128 64 0
White = Materiales(color(1, 1, 1), [0.9, 0.1], 5)
blueish_sphere = Materiales(color(0,71/255,171/255), [0.7, 0.3], 50)

Brown = Materiales(color(128/255, 64/255, 0), [0.8, 0.2], 50)
red_sphere = Materiales(diff=color(1,0,0), albedo=(0.6, 0.3, 0.1,0), spec=35, )

black = Materiales(color(0, 0, 0), [1, 0], 0)

rt.light = Light( glMatematica.Normalizar(V3(0, 0, 0))  ,   1 , color(1,1,1))
rt.background_color = color(0.4,0.4,0.4)

rt.items = [
    Plane(V3(0,2,0), 50,50,red_sphere)
]

rt.rtRender()
rt.glFinish('rtOUT.bmp')

