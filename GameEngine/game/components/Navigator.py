'''
Created on Feb 18, 2014

@author: otrebor
'''
from game.components import Component

class Navigator(Component.ComponentBase):
    
    def __init__(self, gameObject):
        Component.ComponentBase.__init__(self, gameObject)
        self.path = None
        
    def setPath(self,dest):
        if self.gameObject.shape:
            if not self.gameObject.world.terrain.validPosition(dest):
                return None
            
            pos = self.gameObject.shape.position.xy()
            self.path = self.gameObject.world.terrain.getPath(pos, dest)
            if self.path:
                self.path.init()
        else:
            print "gameObject don't have shape"
    
            
        
        