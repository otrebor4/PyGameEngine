'''
Created on Feb 11, 2014

@author: Otrebor45
'''
import pygame
import Component
import gameEngine.phys.shapes.Polygon as Polygon

#general light class
class Light(Component.Component):
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.light = None
        self.position = (0,0)
        self.offset = (0,0)
        
    def update(self, delta):
        if self.light != None:
            pos = self.gameObject.shape.position.xy() if self.gameObject.shape else self.position
            pos = (pos[0]+self.offset[0], pos[1]+self.offset[1])
            terrain = self.gameObject.world.terrain
            terrain.addLight(self.light, pos)
 
#creates a cone light from an object       
class FlashLight(Component.Component):
    
    def __init__(self,gameObject):
        Component.Component.__init__(self, gameObject)
        self.color = (255,255,255,255)
        self.widht = 10
        self.height = 10
        self.angle = 0
        self.offset = (0,0)
        self.catche = None
        self.catcheAngle = 0
        self.startHeight = 0
        
    def setVals(self, width, height, angle, color,start=0, offset=(0,0)):
        self.color = color
        self.height = height
        self.widht = width
        self.angle = angle
        self.offset = offset
        self.startHeight =start
        
    def makePolygon(self):
        if self.catche is None:
            points = [ (0,0),(0,-self.startHeight/2) , (self.widht,-self.height/2), (self.widht, self.height/2),(0, self.startHeight/2) ]
            ((x,y),pt) = Polygon.getPolygonFromPoints(points)
            self.catche = Polygon.Polygon(self.gameObject.transform, (x,y), pt)
        return self.catche
    
    '''
    TODO:Need fix and use shape angle and offset instead
    '''
    def update(self,delta):
        if not self.catche or self.catcheAngle != self.angle:
            self.catche = self.makePolygon()
            self.catche.angle = self.angle
            self.catcheAngle = self.angle
        polygon = self.catche
        offset = (0-polygon.left,0- polygon.top)
        points = polygon.pointlist
        points = self.addOffSet(points,offset)
        w=polygon.width
        h=polygon.height
        light = pygame.Surface( (w,h), pygame.SRCALPHA,32)
        light.fill( (0,0,0,0))
        pos = self.gameObject.transform.position.xy() if self.gameObject.transform.position else (0,0)
        pos = (pos[0]+self.offset[0]-offset[0], pos[1]+self.offset[1]-offset[1])
        pygame.draw.polygon(light, self.color, points )
        self.gameObject.world.terrain.addLight(light,pos)
            
    def addOffSet(self, pts, offset):
        points = []
        for pt in pts:
            points.append( (pt[0]+offset[0], pt[1]+offset[1]))
        return points
 
#light for the entire area in play   
class EnvironmentLight(Component.Component):
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.color = (10,10,10,255)
        
    def setVal(self, lightColor= (10,10,10,255)):
        self.color = lightColor
        
    def update(self,delta):
        light = pygame.display.get_surface().convert_alpha()
        light.fill(self.color)
        self.gameObject.world.terrain.addLight(light,(0,0))
        
class SpotLight(Component.Component):        
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.position = None
        self.radius = 1
        self.color = (255,255,255,255)
        self.offset = (0,0)
        
    def setVals(self, radius, color, offset):
        self.radius = radius
        self.color = color
        self.offset = offset
        
    def update(self,delta):
        pos = self.position if self.position != None else (self.gameObject.shape.Center().xy() if self.gameObject.shape != None else (0,0))                                                 
        light = pygame.Surface( ( 2*self.radius,2*self.radius),pygame.SRCALPHA, 32)
        light.fill((0,0,0,0))
        pygame.draw.circle(light, self.color, (self.radius,self.radius),self.radius)
        pos = (pos[0]-self.radius+self.offset[0], pos[1]-self.radius+self.offset[1])
        self.gameObject.world.terrain.addLight(light,pos)
        
        
        