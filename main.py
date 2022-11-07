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
anaranjado = color(1, 0.6, 0)
negro = color(0, 0, 0)
rojo = color(1,0,0)

#partes para formar el snowman
rt.items = [
    sphere(V3(0, -3.5, -16), 1.5, blanco),
    sphere(V3(0, -0.4, -16), 2, blanco),
    sphere(V3(0, 2.5, -16), 3, blanco),
    sphere(V3(0.8, -4, -16), 0.3, negro),
    sphere(V3(-0.8, -4, -16), 0.3, negro),
    sphere(V3(0, -1, -16), 0.15, negro),
    sphere(V3(0, -0.5, -16), 0.15, negro),
    sphere(V3(0, 0, -16), 0.15, negro),
    sphere(V3(0, -3.5, -16), 0.3, anaranjado),
    sphere(V3(0, -5, -16), 0.3, rojo),
    sphere(V3(0.5, -5, -16), 0.3, rojo),
    sphere(V3(1, -5, -16), 0.3, rojo),
    sphere(V3(-0.5, -5, -16), 0.3, rojo),
    sphere(V3(-1, -5, -16), 0.3, rojo),
    sphere(V3(1.5, -5, -16), 0.3, rojo),
    sphere(V3(-1.5, -5, -16), 0.3, rojo),
    sphere(V3(2, -5, -16), 0.3, rojo),
    sphere(V3(-2, -5, -16), 0.3, rojo),
    sphere(V3(0, -6, -16), 1, rojo),
]

rt.rtRender()
rt.glFinish('rtOUT.bmp')

