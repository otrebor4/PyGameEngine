'''
Created on Jan 22, 2014

@author: otrebor
'''
'''
physical object template
'''

import game.components.Component as Component
import game.phys.shapes.Rectangle as Rectangle
import game.phys.shapes.Circle as Circle
import game.phys.shapes.Polygon as Polygon

# collider depends on shape to determine its position,size,dimensions
#
class Collider(Component.Component):
    taml_tag = u'Collider'
    def __getstate__(self):
        data = Component.Component.__getstate__(self)
        data['static'] = self.static
        data['isTrigger'] = self.isTrigger
        return data
    
    
    
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.gameObject.collider = self
        self.gameObject.shape = None
        self.static = False
        self.isTrigger =False
        
        
    def draw(self, screen):
        if self.gameObject and self.gameObject.shape:
            self.gameObject.shape.draw(screen)
    
class CircleCollider(Collider):
    yaml_tag = u'!CircleCollider'
    def __init__(self, gameObject, x=0, y=0, radius=0):
        Collider.__init__(self, gameObject)
        self.gameObject.shape = Circle.Circle(x, y, radius)
        
class RectCollider(Collider):
    yaml_tag = u'!RectCollider'
    def __init__(self, gameObject, x=0, y=0, w=0, h=0):
        Collider.__init__(self, gameObject)
        self.gameObject.shape = Rectangle.Rectangle(x, y, w, h)
        
class PolygonCollider(Collider):
    yaml_tag = u'!PolygonCollider'
    def __init__(self, gameObject, x=0, y=0, points=[]):
        Collider.__init__(self, gameObject)
        self.gameObject.shape = Polygon.Polygon(x, y, points)
        
