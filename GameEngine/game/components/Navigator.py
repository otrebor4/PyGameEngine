'''
Created on Feb 18, 2014

@author: otrebor
'''
import Component
#import Render
class Navigator(Component.Component):
    
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        
        self.path = None
        
    def SetPath(self,dest):
        if self.gameObject.shape:
            if not self.gameObject.world.terrain.validPosition(dest):
                return None
            
            pos = self.gameObject.shape.position.xy()
            self.path = self.gameObject.world.terrain.GetPath(pos, dest)
            if self.path:
                self.path.init()
        else:
            print "gameObject don't have shape"
    
    #def draw(self, screen):
    #    if self.path:
    #        self.path.draw(screen)
            
        
        