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
White = Materiales(diff=color(1, 1, 1), albedo=(0.6, 0.3, 0.1,0), spec=35, )
blueish_sphere = Materiales(color(0,71/255,171/255), [0.7, 0.3], 50)

Brown = Materiales(color(128/255, 64/255, 0), [0.8, 0.2], 50)
red_sphere = Materiales(diff=color(1,0,0), albedo=(0.6, 0.3, 0.1,0), spec=35, )

black = Materiales(color(0, 0, 0), [1, 0], 0)

rt.light = Light( glMatematica.Normalizar(V3(0, 0, 1))  ,   1 , color(1,1,1))
rt.background_color = color(0.4,0.4,0.4)

rt.items = [
    cube((0.75, 0.10 ,-3), V3(0.5,0.5,0.5), red_sphere)
]

translation = (0,0.2,0)
scale = (0.5,0.5,0.5)
rotation = ( 0.5, 1, 0 )

rt.lookAT(V3(0,0,5), V3(0,0,0), V3(0,1,0))


rt.rtRender()
rt.LoadModel('./objs/creeper.obj', translation, scale, rotation,)
rt.glFinish('rtOUT.bmp')

