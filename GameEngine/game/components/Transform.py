'''
Created on Feb 27, 2014

@author: rfloresx
'''
import game.util.Vector2 as Vector2
import Component
#work in progress
class Transform(Component.Component):
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self._local_position = Vector2.Zero
        self._parent = None
        self._childs = []
        self._rotation = 0
        
    def _addChild(self,value):
        if value not in self._childs:
            self._childs.append(value)
    
    def _removeChild(self,value):
        if value in self._childs:
            self._childs.remove(value)
                   
    @property
    def parent(self):
        return self._parent
    @parent.setter
    def parent(self,value):
        pos = self.position #get current position
        if self.parent:
            self._parent._removeChild(self) 
        self._parent = value
        if self._parent:
            self._parent._addChild(self)
        self.position = pos #set position and fix local_position
   
    @property
    def localPosition(self):
        return self._local_position
    @localPosition.setter
    def localPosition(self,value):
        self._local_position = value
    
    @property
    def rotation(self):
        return self._rotation
    @rotation.setter
    def rotation(self,value):
        self._rotation = value
        
    @property
    def parentRotation(self):
        return self.parent.rotation if self.parent else 0
    @parentRotation.setter
    def parentRoation(self,value):
        if self.parent:
            self.parent.rotatoin = value
        
    @property
    def position(self):
        if self._parent:
            return self._parent.position.add(self.localPosition.rotate(self.parent.rotation))
        else:
            return self.localPosition
    @position.setter
    def position(self,value):
        if self._parent:
            offset = value.rotate(-self.parent.rotation).sub(self._parent.position)
            self.localPosition = offset
        else:
            self.localPosition = value
    