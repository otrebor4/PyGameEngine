'''
Created on Jan 28, 2014

@author: otrebor
'''
import gameEngine.components.Transform as Transform
import gameEngine.util.Vector2 as Vector2

class Shape:
    def __init__(self,transform):
        self.transform = Transform.Transform(None)
        self.transform =transform
        self.aabb = (0, 0, 0, 0)
    
    @property
    def collider(self):
        if self.transform.gameObject:
            return self.transform.gameObject.collider
        return None
    
    @property
    def position(self):
        return self.transform.position

    '''
    =========AABB useful variables
    '''
    @property
    def left(self):
        return self.aabb[0]
        
    @property
    def top(self):
        return self.aabb[1]
    
    @property
    def right(self):
        return self.aabb[2]
    
    @property
    def bottom(self):
        return self.aabb[3]
    
    @property
    def width(self):
        return self.right - self.left
    
    @property
    def height(self):
        return self.bottom - self.top
    
    @property
    def startCorner(self):
        return Vector2.Vector2(self.left, self.top)
    
    @property
    def endCorner(self):
        return Vector2.Vector2(self.right, self.bottom)
    
    #aabb stands for axis align bounding box
    def calAABB(self):
        raise NotImplementedError

    @property
    def center(self):
        raise NotImplementedError
    @property    
    def radius(self):
        raise NotImplementedError
    @property
    def points(self):
        raise NotImplementedError
    
    def draw(self, screen):
        raise NotImplementedError
    
            
            