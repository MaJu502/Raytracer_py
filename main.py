"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
se usan valores de 0 a 1 para los colores en esta version
"""
from ray import *
from sphere import *
from vectors import *

rt = Raytracer(700,700)
rt.glClear()

#colores del snowman
blanco = color(1, 1, 1)
anaranjado = color(0.7, 0.5, 0)
negro = color(0, 0, 0)

#partes para formar el snowman
rt.items = [
    sphere(V3(0, -4, -16), 2, blanco),
    sphere(V3(0, -0.4, -16), 3, blanco),
    sphere(V3(0, 3.8, -16), 4, blanco),
    sphere(V3(0, -3.6, -16), 0.18, anaranjado),
    sphere(V3(0.8, -4.6, -16), 0.2, negro),
    sphere(V3(-0.8, -4.6, -16), 0.2, negro),
]

rt.rtRender()
rt.glFinish('rtOUT.bmp')

