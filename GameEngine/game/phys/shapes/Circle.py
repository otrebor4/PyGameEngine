'''
Created on Jan 28, 2014

@author: otrebor
'''
import Shape
import game.util.Vector2 as Vector2

class Circle(Shape.Shape):
    yaml_tag = u'!Circle'
    def __getstate__(self):
        data = Shape.Shape.__getstate__(self)
        data['radius'] = self.radius
        return data
    
    def __init__(self, transform, (x,y) =(0,0), r=0):
        Shape.Shape.__init__(self, transform)
        self._offset = (x,y)
        self.aabb = [-r, -r, r, r]
        self._radius = r
        
    def calAABB(self):
        self.aabb = [-self.radius, -self.radius, self.radius, self.radius]
    
    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self,value):
        self._offset = value
        
    @property
    def center(self):
        return self.transform.position.add(Vector2.Vector2(*self.offset))
    
    @property
    def width(self):
        return self.radius*2
    
    @property
    def height(self):
        return self.radius*2
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self,value):
        self._radius = value
        self.calAABB()
    
    