'''
Created on Feb 27, 2014

@author: rfloresx
'''
import game.util.Vector2 as Vector2

class Transform:
    def __init__(self):
        self._local_position = Vector2.Zero
        self._parent = None
        #self.position = (0,0)
        #self.localPosition = (0,0)
        #self.parent = None
    
    @property
    def localPosition(self):
        return self._local_position
    @localPosition.setter
    def localPosition(self,value):
        self._local_position = value
        
    @property
    def position(self):
        if self._parent:
            return self._parent.position.add(self.localPosition)
        else:
            return self.localPosition
    @position.setter
    def position(self,value):
        if self._parent:
            offset = value.sub(self._parent.position)
            self.localPosition = offset
        else:
            self.localPosition = value
    
    @property
    def rotation(self):
        return self._rotation