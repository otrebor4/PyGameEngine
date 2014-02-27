'''
Created on Jan 28, 2014

@author: otrebor
'''
import Shape


class Circle(Shape.Shape):
    yaml_tag = u'!Circle'
    def __getstate__(self):
        data = Shape.Shape.__getstate__(self)
        data['radius'] = self.radius
        return data
    
    def __init__(self, x=0, y=0, r=0):
        Shape.Shape.__init__(self, x, y)
        # that simple, note aabb is not actual world position
        self.aabb = [-r, -r, r, r]
        self.radius = r
        
    def Radius(self):
        return self.radius