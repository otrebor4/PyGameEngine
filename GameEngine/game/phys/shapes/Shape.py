'''
Created on Jan 28, 2014

@author: otrebor
'''
import game.lib.yaml as yaml
import game.components.Transform as Transform


class Shape(yaml.YAMLObject):
    yaml_tag = u'!Shape'
    def __getstate__(self):
        data = {}
        data['position'] = self.position
        data['aabb'] = self.aabb
        return data
    
    def __init__(self,transform):
        self.transform = Transform.Transform(None)
        self.transform =transform
        self.aabb = (0, 0, 0, 0)
    
    '''
    =========AABB useful variables
    '''
    @property
    def position(self):
        return self.transform.position
    
    #aabb stands for axis align bounding box
    def calAABB(self):
        raise NotImplementedError
    
    @property
    def left(self):
        raise NotImplementedError
    
    @property
    def top(self):
        raise NotImplementedError
    @property
    def right(self):
        raise NotImplementedError
    @property
    def bottom(self):
        raise NotImplementedError
    @property
    def width(self):
        raise NotImplementedError
    @property
    def height(self):
        raise NotImplementedError
    @property
    def center(self):
        raise NotImplementedError
    @property
    def startCorner(self):
        raise NotImplementedError
    @property    
    def radius(self):
        raise NotImplementedError
    
    def draw(self, screen):
        raise NotImplementedError
    @property
    def points(self):
        raise NotImplementedError
        
            
            