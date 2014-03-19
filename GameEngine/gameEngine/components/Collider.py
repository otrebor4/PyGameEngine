'''
Created on Jan 22, 2014

@author: otrebor
'''
'''
physical object template
'''

import gameEngine.components.Component as Component
import gameEngine.phys.shapes.Rectangle as Rectangle
import gameEngine.phys.shapes.Circle as Circle
import gameEngine.phys.shapes.Polygon as Polygon

#Collider components define the shape of an object for the purposes of physical collisions
#Collider depends on shape to determine its position,size,dimensions
class Collider(Component.Component):    
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        if self.gameObject:
            self.gameObject.collider = self
        self.isStationary = False
        self.isTrigger = False  
        self.shape = None
        
    def draw(self, screen):
        if self.shape:
            self.shape.draw(screen)
    
    def calAABB(self):
        return self.shape.calAABB() if self.shape else None
    
    def getPoints(self):
        if self.shape:
            return self.shape.points
        return []
    
    '''
    =========AABB useful variables
    '''
    @property
    def left(self):
        return self.shape.left if self.shape else None
        
    @property
    def top(self):
        return self.shape.top if self.shape else None
    
    @property
    def right(self):
        return self.shape.right if self.shape else None
    
    @property
    def bottom(self):
        return self.shape.bottom if self.shape else None
    
    @property
    def width(self):
        return self.shape.width if self.shape else None
    
    @property
    def height(self):
        return self.shape.height if self.shape else None
    
    @property
    def startCorner(self):
        return self.shape.startCorner if self.shape else None
    
    @property
    def endCorner(self):
        return self.shape.endCorner if self.shape else None
    
    @property
    def center(self):
        return self.shape.center if self.shape else None
    
    @property    
    def radius(self):
        return self.shape.radius if self.shape else None
    
    @property
    def points(self):
        return self.shape.points if self.shape else None

    
    
class CircleCollider(Collider):
    def __init__(self, gameObject, x=0, y=0, radius=0):
        Collider.__init__(self, gameObject)
        self.shape = Circle.Circle(self.transform, (x, y), radius)
        
class PolygonCollider(Collider):
    def __init__(self, gameObject, x=0, y=0, points=[]):
        Collider.__init__(self, gameObject)
        self.shape = Polygon.Polygon(self.transform, (0, 0), points)
        
class RectCollider(PolygonCollider):
    def __init__(self, gameObject, x=0, y=0, w=0, h=0):
        Collider.__init__(self, gameObject)
        self.shape = Rectangle.Rectangle(self.transform, (x, y), (w, h))       
