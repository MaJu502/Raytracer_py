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
water = Materiales(color(0,71/255,1), albedo=(0.6, 0.3, 0.8,0), spec=35,)
grama = Materiales(diff=color(0, 1, 0), albedo=(0.6, 0.3, 0.1,0), spec=35, )
leaves = Materiales(diff=color(0, 100/255, 0), albedo=(0.6, 0.3, 0.1,0), spec=35, )
Brown = Materiales(diff=color(128/255, 64/255, 0), albedo=(0.5, 0.3, 0,0), spec=1, refractive_index=0.1)
sand = Materiales(diff=color(76/255, 60/255, 50/255), albedo=(0.9, 0.4, 0.1,0.5), spec=1, refractive_index=0.1)
torch = Materiales(diff=color(1,215/255,0), albedo=(0.6, 0.3, 0.8,0), spec=35, )
sky = Materiales(color(0,144/255,1), albedo=(0.6, 0.3, 0.8,0), spec=35,)

black = Materiales(color(0, 0, 0), [1, 0], 0)

rt.light = Light( glMatematica.Normalizar(V3(0, 0, 1))  ,   1 , color(1,1,1))
rt.background_color = color(0.4,0.4,0.4)

rt.items = [
    cube((-0.18, 0.10 ,-0.825), V3(0.06,0.005,0.08), water),
    cube((0.13, -0.05 ,-1.1), V3(0.3,0.1,0.3), leaves),
    cube((0.15, -0.09 ,-1.1), V3(0.08,0.1,0.08), leaves),
    cube((0.15, -0.05 ,-1.1), V3(0.2,0.1,0.4), leaves),
    cube((0.15, -0.05 ,-1.1), V3(0.4,0.1,0.2), leaves),
    cube((-0.15, 0.10 ,-0.6), V3(0.15,0.005,0.15), sand),
    cube((-0.15, 0.06 ,-0.45), V3(0.02,0.02,0.02), sand),
    cube((0.15, 0.10 ,-1.1), V3(0.08,0.2,0.08), Brown),
    cube((0.08, 0.10 ,-0.45), V3(0.005,0.02,0.005), Brown),
    cube((0.08, 0.085 ,-0.45), V3(0.005,0.005,0.005), torch),
    cube((-0.15, 0.10 ,-0.72), V3(0.15,0.005,0.10), water),
    cube((0.08, 0.15 ,-0.45), V3(10,0.005,2), grama)
]

#objeto
translation = (-0.5,-0.3,0)
scale = (0.1,0.1,0.1)
rotation = ( -0.4, -0.9, 0 )
rt.lookAT(V3(0,50,50), V3(0,0,0), V3(0,1,0))


rt.rtRender()
rt.LoadModel('./objs/creeper.obj', translation, scale, rotation,)
rt.glFinish('rtOUT.bmp')

