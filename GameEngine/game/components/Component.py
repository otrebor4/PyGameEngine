'''
Created on Jan 28, 2014

@author: otrebor
'''

#Base class for a component
class Component(object):

    def __init__(self, gameObject):
        self.gameObject = gameObject
        if self.gameObject != None:
            self.gameObject.components.append(self)
    
    def update(self, delta):
        pass
    
    def Destroy(self):
        if self.gameObject:
            self.gameObject.Destroy()

    @property
    def position(self):
        if self.gameObject:
            return self.gameObject.transform.position
        return None
    @position.setter
    def position(self,value):
        if self.gameObject:
            self.gameObject.transform.position = value

    @property
    def transform(self):
        if self.gameObject:
            return self.gameObject.transform
        return None
    
    @property
    def collider(self):
        if self.gameObject:
            return self.gameObject.collider
        return None
    
    @property
    def rigid(self):
        if self.gameObject:
            return self.gameObject.rigid
        return None