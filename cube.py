"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
    cube.py
"""
from sphere import Materiales,Intersect
import glMatematica
class cube:
    def __init__(self, center, w, material):
        self.center = center
        self.material = material
        self.scale = w
        #