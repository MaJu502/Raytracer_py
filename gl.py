"""
Universidad del Valle de Guatemala 
@author Marco Jurado 20308
"""

from collections import namedtuple
import struct

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
    return bytes([b, g, r])

Black = color(0,0,0)
White = color(1,1,1)
V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])



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

    print(' DIOOOOOOOOOOS ESTAAAAAAA AQUIIIIIIII...')
    op.close()

def glFinishZBuffer(self,filename):
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
            temp = self.zbuffer[y][x]
            temp = int(temp)
            if temp < 0:
                temp = 0
            if temp > 255:
                temp = 255
            temp2 = color(temp,temp,temp)
            op.write(temp2)

    op.close()
