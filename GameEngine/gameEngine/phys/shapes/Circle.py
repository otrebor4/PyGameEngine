'''
Created on Jan 28, 2014

@author: otrebor
'''
import Shape
import gameEngine.util.Vector2 as Vector2
import pygame


class Circle(Shape.Shape):
    
    def __init__(self, transform, (x,y) =(0,0), r=0):
        Shape.Shape.__init__(self, transform)
        self._offset = (x,y)
        self.aabb = [-r, -r, r, r]
        self._radius = r
        self.calAABB()
        
    def calAABB(self):
        self.aabb = [-self.radius+self.center.x, -self.radius+self.center.y, self.radius+self.center.x, self.radius+self.center.y]
        return self.aabb
    
    
    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self,value):
        if self._offset != value:
            self._offset = value
            self.calAABB()
        
    @property
    def center(self):
        return self.transform.position.add(Vector2.Vector2(*self.offset))
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self,value):
        if self._radius != value:
            self._radius = value
            self.calAABB()
    
    @property
    def points(self):
        points = []
        start = Vector2.Vector2(self.radius,0)
        points.append(start)
        angle = 0
        while angle < 360:
            points.append(start.rotate(angle) )
            angle += 30
        return points
            
    def draw(self, screen):
        color = (255,0,0,100)
        pos = self.center
        pygame.draw.circle(screen, color, (int(pos.x),int(pos.y)), int(self.radius))
        vt = Vector2.Right
        vt = vt.rotate(self.transform.rotation).scale(self.radius)
        c = self.center
        vt = vt.add(c)
        pygame.draw.aaline(screen, (0,255,0), ( int(c.x),int(c.y)), (int(vt.x),int(vt.y)) )
    