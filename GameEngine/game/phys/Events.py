'''
Created on Feb 16, 2014

@author: Otrebor45
'''
#object on object collision
class OnCollision:
    def __init__(self, other, normal, distance):
        self.other = other
        self.normal = normal
        self.distance = distance
        
    def CallOn(self,gameObject):
        gameObject.sendMessage("OnCollision", self)

#object on boundary collision 
class OnTrigger:
    def __init__(self, other, normal, distance):
        self.other = other
        self.normal = normal
        self.distance = distance
        
    def CallOn(self,gameObject):
        gameObject.sendMessage("OnTrigger", self)     