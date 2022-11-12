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

#materiales para osos 128 64 0
White = Materiales(color(1, 1, 1), [0.9, 0.1], 5)
blueish_sphere = Materiales(color(0,71/255,171/255), [0.7, 0.3], 50)

Brown = Materiales(color(128/255, 64/255, 0), [0.8, 0.2], 50)
red_sphere = Materiales(color(1,0,0), [0.6, 0.4], 35)

black = Materiales(color(0, 0, 0), [1, 0], 0)

rt.light = Light( glMatematica.Normalizar(V3(0, 0, 0))  ,   1 , color(1,1,1))
rt.background_color = color(0.4,0.4,0.4)

rt.items = [
    sphere(V3(-2.5, -2.5 + 2.2, -9), 1.4, blueish_sphere),
    sphere(V3(-3.3, -1, -8), 0.5, White),
    sphere(V3(-1.2, -1, -8.4), 0.5, White),
    sphere(V3(-3, 0.7, -8), 0.5, White),
    sphere(V3(-1.5, 0.7, -8), 0.5, White),
    sphere(V3(-2.28, -1.7, -8), 0.9, White),
    sphere(V3(-2.65, -2.4, -7.5), 0.4, White),
    sphere(V3(-1.65, -2.4, -7.8), 0.4, White),
    sphere(V3(-2.3, -1.65, -7.2), 0.1, black),
    sphere(V3(-1.85, -1.65, -7.2), 0.1, black),
    sphere(V3(-2.17, -1.35, -7.55), 0.25, White),
    sphere(V3(-2.08, -1.3, -7.2), 0.08, black),

    sphere(V3(2, -2.5 + 2.2, -9), 1.4, red_sphere),
    sphere(V3(0.8, -1, -8), 0.5, Brown),
    sphere(V3(3.2, -1, -8.4), 0.5, Brown),
    sphere(V3(1, 0.7, -8), 0.5, Brown),
    sphere(V3(2.5, 0.7, -8), 0.5, Brown),
    sphere(V3(1.72, -1.7, -8), 0.9, Brown),
    sphere(V3(1.15, -2.4, -7.6), 0.4, Brown),
    sphere(V3(2.15, -2.4, -7.5), 0.4, Brown),
    sphere(V3(1.4, -1.65, -7.2), 0.1, black),
    sphere(V3(1.85, -1.65, -7.2), 0.1, black),
    sphere(V3(1.7, -1.35, -7.55), 0.25, Brown),
    sphere(V3(1.65, -1.3, -7.2), 0.08, black),
]

rt.rtRender()
rt.glFinish('rtOUT.bmp')

