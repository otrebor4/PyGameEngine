'''
Created on Feb 5, 2014

@author: Otrebor45
'''
import Component
class Render(Component.Component):
    yaml_tag = u'!Render'
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        if gameObject:
            gameObject.renders.append(self)
    
    def draw(self, screen):
        pass

class GUIComponent(Render):
    yaml_tag = u'!GUIComponent'
    
    def __init__(self,gameObject):
        Render.__init__(self, gameObject)
        if gameObject:
            gameObject.GUIs.append(self)
        
    def OnGUI(self,screen):
        pass