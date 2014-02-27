'''
Created on Feb 11, 2014

@author: Otrebor45
'''
import pygame
import Component
import game.phys.shapes.Polygon as Polygon

class Light(Component.Component):
    yaml_tag = u'!Light'
    def __getstate__(self):
        data = Component.Component.__getstate__(self)
        data['light'] = self.light
        data['position'] = self.position
        return data
    
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
            terrain.AddLight(self.light, pos)
        
class FlashLight(Component.Component):
    
    def __init__(self,gameObject):
        Component.Component.__init__(self, gameObject)
        self.intensity = 0
        self.widht = 10
        self.height = 10
        self.angle = 0
        self.offset = (0,0)
        self.catche = None
        self.catcheAngle = 0
        self.startHeight = 0
    def setVals(self, width, height, angle, intensity,start=0, offset=(0,0)):
        self.intensity = intensity
        self.height = height
        self.widht = width
        self.angle = angle
        self.offset = offset
        self.startHeight =start
        
    def makePolygon(self):
        points = [ (0,0),(0,-self.startHeight/2) , (self.widht,-self.height/2), (self.widht, self.height/2),(0, self.startHeight/2) ]
        ((x,y),pt) = Polygon.getPoligonFromPoints(points)
        return Polygon.Polygon( x,y, pt)
    
    def update(self,delta):
        if not self.catche or self.catcheAngle != self.angle:
            self.catche = self.makePolygon().rotate(self.angle)
            self.catcheAngle = self.angle
        polygon = self.catche
        
        
        offset = (0-polygon.Left(),0- polygon.Top())
        points = polygon.Points()
        points = self.AddOffSet(points,offset)
        w=polygon.Width()
        h=polygon.Height()
        light = pygame.Surface( (w,h), pygame.SRCALPHA,32)
        light.fill( (255,255,255,255))
        color = (255,255,255,255-self.intensity)
        pos = self.gameObject.shape.position.xy() if self.gameObject.shape else (0,0)
        pos = (pos[0]+self.offset[0]-offset[0], pos[1]+self.offset[1]-offset[1])
        
        pygame.draw.polygon(light, color, points )
        self.gameObject.world.terrain.AddLight(light,pos)
            
    def AddOffSet(self, pts, offset):
        points = []
        for pt in pts:
            points.append( (pt[0]+offset[0], pt[1]+offset[1]))
        return points
        #pos = self.position if self.position != None else (self.gameObject.shape.Center().xy() if self.gameObject.shape != None else (0,0))
        #light = 
        #light = pygame.Surface( ( 2*self.radius,2*self.radius),pygame.SRCALPHA, 32)
        #light.fill((255,255,255,255))
        #pygame.draw.polygon(light,(255,255,255,255-self.intensity), self.GetPoints(pos),  ) #circle(light, (255,255,255,255-self.intensity), (self.radius,self.radius),self.radius)
        #pos = (pos[0]-self.radius, pos[1]-self.radius)
        #self.gameObject.world.terrain.AddLight(light,pos)
    
class EnvironmentLight(Component.Component):
    yaml_tag = u'!EnvironmentLight'
    def __getstate__(self):
        data = Component.Component.__getstate__(self)
        data['color'] = self.color
        return data
    
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.color = (0,0,0,10)
        
        
    def update(self,delta):
        light = pygame.display.get_surface().convert_alpha()
        light.fill(self.color)
        self.gameObject.world.terrain.AddLight(light,(0,0))
        
class SpotLight(Component.Component):
    yaml_tag = u'!SpotLight'
    def __getstate__(self):
        data =  Component.Component.__getstate__(self)
        data['position'] = self.position
        data['radius'] = self.radius
        data['intensity'] = self.intensity
        return data
        
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.position = None
        self.radius = 1
        self.intensity = 0
        self.offset = (0,0)
        
    def setVals(self, radius, intensity, offset):
        self.radius = radius
        self.intensity = intensity
        self.offset = offset
        
    def update(self,delta):
        pos = self.position if self.position != None else (self.gameObject.shape.Center().xy() if self.gameObject.shape != None else (0,0))
                                                               
        light = pygame.Surface( ( 2*self.radius,2*self.radius),pygame.SRCALPHA, 32)
        light.fill((255,255,255,255))
        pygame.draw.circle(light, (255,255,255,255-self.intensity), (self.radius,self.radius),self.radius)
        pos = (pos[0]-self.radius+self.offset[0], pos[1]-self.radius+self.offset[1])
        self.gameObject.world.terrain.AddLight(light,pos)
        
        
        