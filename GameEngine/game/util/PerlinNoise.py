'''
Created on Feb 23, 2014

@author: otrebor
'''

import pygame
import sys
import perlin
import random
import math

def Noise(x,y):
    n = x+y * 57;
    n = (n<<13)^n
    return ( 1.0 -( (n*(n*n*15731+789221) + 1376312589) & 0x7ffffffff)/1073741824.0)

def Noise1(x,y):
    n = x+y * 57;
    n = (n<<13)^n
    return ( 1.0 -( (n*(n*n*15731+789221) + 1376312589) & 0x8ffffffff)/1073741824.0)

def avg(m_map, x,y):
    v = m_map[x-1][y]
    v += m_map[x][y-1]
    v += m_map[x+1][y]
    v += m_map[x][y+1]
    v += m_map[x][y]*2
    return v/6

def smoth(m_map,width,height, times = 1):
    for x in range(0,times):
        for x in range(1,width-1):
            for y in range(1,height-1):
                m_map[x][y] = avg(m_map,x,y)
    return m_map 

def makenoise( width,height, x, y, z):
    m_map = []
    for i in range(0,width):
        for j in range(0,height):
            cx = i + x
            cy = j + y
            n = perlin.SimplexNoise()
            f = n.noise2(cx,cy)*2
            #f += n.noise2(cx+z,cy)*0.25
            #f += n.noise2(cx,cy+z)*0.25
            #f += n.noise2(cx+z,cy+z)*0.25
            #f /= 2
            if i >= len(m_map):
                m_map.append([])
            m_map[i].append( f)
    return smoth(m_map, width, height, 2)

def makeMap(width,height):
    m_map = []
    for x in range(0,width):
        m_map.append([])
        for y in range(0,height):
            m_map[x].append(0.0)
    return m_map
            
def expand(m_map,width,height, exp):
    m_map1 = []
    for x in range(0,width):
        for y in range(0,height):
            f = m_map[x][y]
            for i in range(0,exp):
                cx = x*exp+i
#                cy = x*exp+i
                if cx >= len(m_map1):
                    m_map1.append([])
                for i in range(0,exp):
                    m_map1[cx].append(f)    
    return m_map1

def normalise(m_map, width,height, Min,Max ):
    tx = width
    ty = height
    highestPoint = 0.0
    lowestPoint = 1.0
    for My in range(0,ty):
        for Mx in range(0,tx):
            h = m_map[Mx][My]
            if h < lowestPoint:
                lowestPoint = h
            elif h > highestPoint:
                highestPoint = h
    heightRange = highestPoint - lowestPoint
    #heightRange = (heightRange if heightRange != 0 else 0.000001)
    normalRange = Max - Min
    for My in range(0,ty):
        for Mx in range(0,tx):
            nh = ( (m_map[Mx][My] - lowestPoint) / heightRange) * normalRange
            m_map[Mx][My] = Min + nh
    return m_map

def generatePerlin(m_map, width,height, octaves,freq,Amp, x = 0, y=0,seed= None):
    tw = width
    th = height
    for y in range(0, height):
        for x in range(0, width):
            m_map[x][y] = 0.0
    noiseFunctions = []
    amp = 1.0
    for i in range(0,octaves):
        noiseFunctions.insert(i, Noise2D(freq,amp, x,y,seed))
        freq *= 2
        amp /=2
        
    for i in range(0,octaves):
        ysteps = float(tw)/float(noiseFunctions[i].frequency)
        xsteps = float(th)/float(noiseFunctions[i].frequency)
        for Px in range(0,tw):
            for Py in range(0,th):
                Pa = int( Px /xsteps)
                Pb = Pa + 1
                Pc = int(Py / ysteps)
                Pd = Pc + 1
                interpValue = noiseFunctions[i].getInterpolatedPoint(Pa, Pb, Pc, Pd, (Px / xsteps) - Pa, (Py / ysteps) - Pc);
                m_map[Px][Py] += interpValue * noiseFunctions[i].amplitude
                
    m_map = normalise(m_map,width,height, 0.0,1.0)
    for Px in range(0,tw):
        for Py in range(0,th):
            m_map[Px][Py] = m_map[Px][Py]*Amp
    #m_map = normalise(m_map,width,height, 0.0,1.0)       
    return m_map
            
class Noise2D:
    def __init__(self,freq,amp, x, y,seed = None):
        #rand = random.Random()
        #rand.seed( seed )
        self.noise = perlin.SimplexNoise( int(math.ceil(2/amp)), seed= seed)# = (x*7351+y*3463)*7919)
        self.frequency = freq
        self.amplitude = amp
        self.noiseValues = []
        for i in range(0,freq):
            self.noiseValues.append([])
            for j in range(0,freq):
                self.noiseValues[i].append( (self.noise.noise2(i+x, j+y)))
                
    def getInterpolatedPointX(self,_xa, _xb, _ya, _yb, Px, Py):
        noise = perlin.SimplexNoise()
                
        noise.noise2(_xa, _ya)    
        return 0
    
    def getInterpolatedPoint(self,_xa, _xb, _ya, _yb, Px, Py):
        i1 = self.interpolate(self.noiseValues[_xa % self.frequency][ _ya % self.frequency], 
                              self.noiseValues[_xb % self.frequency][ _ya % self.frequency], Px);
        i2 = self.interpolate(self.noiseValues[_xa % self.frequency][ _yb % self.frequency], 
                              self.noiseValues[_xb % self.frequency][ _yb % self.frequency], Px);
        return self.interpolate(i1, i2, Py);
    
    def interpolate(self, Pa, Pb, Px):
        ft = Px * math.pi
        f = (1 - math.cos(ft))*0.5
        return Pa * ( 1 - f) + Pb*f
        
    




if __name__ == "__main__":
    seed = 7919
    noises = []
    pygame.init()
    screen = pygame.display.set_mode( (512,512))
    size = 64
    m_map = makeMap(size,size)
    m_map = generatePerlin(m_map,size,size, 8, 4, 1,0,0,seed)
    #m_map = smoth(m_map, size, size, 5)
    noises.append(m_map)
    m_map = makeMap(size,size)
    m_map = generatePerlin(m_map,size,size, 8, 4, 1, 64,64,seed)
    #m_map = smoth(m_map, size, size, 5)
    noises.append(m_map)
    x = 0
    for noise in noises:
        w = h = 4
        for i in range(0,size):
            for j in range(0,size):
                c = noise[i][j]
                c = (c+1.0)/2.0
                c = 0 if c < .33 else (.3 if c < .66 else (.6 if c < .9 else 1))
                #c = 0 if c < 0 else ( 1 if c > 1 else c)
                c = int( (c*255))
                
                rect = (x+i*w, j*h, w, h )
                pygame.draw.rect(screen, (c,c,c), rect)
        x += size*4
        pygame.display.flip()
        pygame.time.wait(500)
        
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    pass