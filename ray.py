"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""

from collections import namedtuple
from math import pi, tan,cos,sin

import struct
import glMatematica
from sphere import *
from vectors import *
from object import Obj

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

        self.View = None
        self.Model = None

        self.glClear()

    def glClear(self):
        self.pixels = [
            [self.background_color for x in range (self.width)] for y in range (self.height)
        ]
        self.zbuffer = [
            [-float('900') for x in range(self.width)] for y in range(self.height)
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
                refract_orig = glMatematica.Suma(intersect.point, offset)

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

    # ------------------------------------------ cargar objetos -----------------------------------------------
    def glTriangle(self, A,B,C, clr=None,textureP=None,cordenadasTextura=(),intensidad=1):
        
        minimo, maximo = glMatematica.Bounding(A, B, C)

        #se debe de definir una nueva intensidad con el movimiento de las camaras
        intensidad = glMatematica.ProdPunto(glMatematica.Normalizar( glMatematica.ProdCruz(glMatematica.Resta(B,A), glMatematica.Resta(C,A))), glMatematica.Normalizar(glMatematica.Resta(V3(0,0,0), self.light.position)))
        intensidad = -intensidad
        #evita llamar la funcion en el caso que la intensidad sea negativa (parte que no recibe nada de luz del modelo)
        if intensidad < 0:
            return
        
        for x in range(round(minimo.x), round(maximo.x) + 1):
            for y in range(round(minimo.y), round(maximo.y) + 1):
                w, v, u = coordenadasbaricentricas(A, B, C, V2(x, y))
                if w < 0 or v < 0 or u < 0:  # 0 is actually a valid value! (it is on the edge)
                    continue
            
                # ahora se cargan las texturas con las coordenadas y la intensidad correspondiente
                if textureP:
                    # si tiene texturas
                    cordA, cordB, cordC = cordenadasTextura
                    tempX = cordA.x * w + cordB.x * v + cordC.x *u
                    tempY = cordA.y * w + cordB.y * v + cordC.y *u

                    clr = textureP.get_color(tempX,tempY, intensidad) # se modifica el color a pintar para ser el correspondiente a la textura

                z = A.z * w + B.z * v + C.z * u

                if x > 0 and x < len(self.zbuffer) and y > 0 and y < len(self.zbuffer[0]):
                    if z > self.zbuffer[x][y]:
                        self.glVertex(x, y, clr)
                        self.zbuffer[x][y] = z


    def LoadModel(self,filename,translation=(0, 0, 0),scale=(1, 1, 1), rotation=(0,0,0), textureP=None):
        # cargar modelo con texturas
        self.loadModelMatrix(translation,scale,rotation)
        model = Obj(filename)
        luz = V3(0,0,1)
        for x in model.faces:
            #cada cara
            temp_vertices = len(x)
            if temp_vertices == 3:
                cara1 = x[0][0] - 1
                cara2 = x[1][0] - 1
                cara3 = x[2][0] - 1

                a = self.transformar(model.vertices[cara1])
                b = self.transformar(model.vertices[cara2])
                c = self.transformar(model.vertices[cara3])
                
                norm = glMatematica.Normalizar( glMatematica.ProdCruz( glMatematica.Resta(b,a) , glMatematica.Resta(c,a) ) )
                
                intensidad = glMatematica.ProdPunto( norm, luz )
                grises = round(intensidad)

                if not textureP:
                    # si el modelo no cuenta con texturas
                    if grises < 0:
                        continue

                    self.glTriangle(a, b, c, color( 85/255,grises,47/255 ))
                
                else: 
                    # si tiene texturas entonces buscamos A B C de las texturas para los triangulos
                    Textura_A = V2(*model.vtvertex[(x[0][1] - 1)])
                    Textura_B = V2(*model.vtvertex[(x[1][1] - 1)])
                    Textura_C = V2(*model.vtvertex[(x[2][1] - 1)])

                    #ahora se dibuja el triangulo
                    self.glTriangle(a,b,c,textureP=textureP, cordenadasTextura=(Textura_A, Textura_B, Textura_C), intensidad=intensidad)

            if temp_vertices == 4:
                cara1 = x[0][0] - 1
                cara2 = x[1][0] - 1
                cara3 = x[2][0] - 1
                cara4 = x[3][0] - 1


                a = self.transformar(model.vertices[cara1])
                b = self.transformar(model.vertices[cara2])
                c = self.transformar(model.vertices[cara3])
                d = self.transformar(model.vertices[cara4])

                
                norm = glMatematica.Normalizar( glMatematica.ProdCruz( glMatematica.Resta(a, b),  glMatematica.Resta(b, c) ) )
                intensidad = glMatematica.ProdPunto( norm, luz )
                grises = (intensidad) - 0.2

                if not textureP:
                    # si el modelo no cuenta con texturas
                    if grises < 0:
                        continue

                    self.glTriangle(a, b, c, color( 85/255,grises,47/255 ))
                    self.glTriangle(a, c, d, color( 85/255,grises,47/255 ))
                
                else: 
                    # si tiene texturas entonces buscamos A B C de las texturas para los triangulos
                    Textura_A = V2(*model.vtvertex[(x[0][1] - 1)])
                    Textura_B = V2(*model.vtvertex[(x[1][1] - 1)])
                    Textura_C = V2(*model.vtvertex[(x[2][1] - 1)])
                    Textura_D = V2(*model.vtvertex[(x[3][1] - 1)])

                    #print('hola1', Textura_A,Textura_B,Textura_C, Textura_D)

                    #ahora se dibuja el triangulo
                    self.glTriangle(a,b,c,textureP=textureP, cordenadasTextura=(Textura_A, Textura_B, Textura_C), intensidad=intensidad)
                    self.glTriangle(a,c,d,textureP=textureP, cordenadasTextura=(Textura_A, Textura_C, Textura_D), intensidad=intensidad)
    
    def lookAT(self, eye, center, up):
        z = ( glMatematica.Normalizar( glMatematica.Resta(eye,center) ) )
        x = ( glMatematica.Normalizar( glMatematica.ProdCruz(up, z) ) )
        y = ( glMatematica.Normalizar( glMatematica.ProdCruz(z,x) ) )
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1/glMatematica.largoVector( glMatematica.Resta(eye,center) ))
        self.loadViewportMatrix()

    def loadViewMatrix(self, x, y, z, center):
        Matriz1 = ([[x.x, x.y, x.z,  0], [y.x, y.y, y.z, 0], [z.x, z.y, z.z, 0], [0, 0, 0, 1]])
        Matriz2 = ([[1, 0, 0, -center.x], [0, 1, 0, -center.y], [0, 0, 1, -center.z], [0, 0, 0, 1]])
        self.View = glMatematica.multiplicarMatriz44(Matriz1, Matriz2)

    def loadProjectionMatrix(self, coeff):
        self.Projection = ([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, coeff, 1]])

    def loadViewportMatrix(self, x = 0, y = 0):
        self.Viewport = ([[self.width/2, 0, 0, x + self.width/2], [0, self.height/2, 0, y + self.height/2], [0, 0, 128, 128], [0, 0, 0, 1]])

    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)
        
        translation_matrix = [[1, 0, 0, translate.x], [0, 1, 0, translate.y], [0, 0, 1, translate.z], [0, 0, 0,1]]
        scale_matrix = [[scale.x, 0, 0, 0], [0, scale.y, 0, 0], [0, 0, scale.z, 0], [0, 0, 0, 1]]
    
        rotar_matrizX = [[1, 0, 0, 0], [0, cos(rotate.x), -sin(rotate.x), 0], [0, sin(rotate.x),  cos(rotate.x), 0],[0, 0, 0, 1]]
        rotar_matrizY = [[cos(rotate.y), 0, sin(rotate.y), 0],[0, 1, 0, 0], [-sin(rotate.y), 0, cos(rotate.y), 0], [0, 0, 0, 1]]
        rotar_matrizZ = [[cos(rotate.z), -sin(rotate.z), 0, 0], [sin(rotate.z),  cos(rotate.z), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

        "con las matrices de x,y,z se puede obtener la matriz de rotacion al multiplicarlas"
        rotation_matrix = glMatematica.multiplicarMatriz44(rotar_matrizX, glMatematica.multiplicarMatriz44(rotar_matrizY, rotar_matrizZ))

        self.Model = glMatematica.multiplicarMatriz44(translation_matrix, glMatematica.multiplicarMatriz44(rotation_matrix, scale_matrix))

    def transformar(self, v):
        tempVertices = [v[0] , v[1], v[2], 1]

        "sustituyendo el uso de numpy para multiplicar estas matrices se reailza lo siguiente"

        temp1 = glMatematica.multiplicarMatriz44(self.Viewport, self.Projection)
        temp2 = glMatematica.multiplicarMatriz44(temp1, self.View)
        temp3 = glMatematica.multiplicarMatriz44(temp2, self.Model)
        temp4 = glMatematica.multiplicarMatriz44(temp3, [ [x] for x in tempVertices ])
        temp4 = [[i[0] for i in temp4]]

        tranformed_vertex = temp4[0]

        tranformed_vertex = [
        (tranformed_vertex[0]/tranformed_vertex[3]), 
        (tranformed_vertex[1]/tranformed_vertex[3]), 
        (tranformed_vertex[2]/tranformed_vertex[3])
        ]

        return V3(*tranformed_vertex)

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
