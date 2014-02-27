'''
Created on Jan 28, 2014

@author: otrebor
'''
import game.lib.yaml as yaml

class Component(yaml.YAMLObject):
    yaml_tag = u'!Component'
    def __getstate__(self):
        data = {}
        data['gameObject'] = self.gameObject
        return data
    
    def __init__(self, gameObject):
        self.gameObject = gameObject
        if self.gameObject != None:
            self.gameObject.components.append(self)
        
    def update(self, delta):
        pass
    
    def Destroy(self):
        if self.gameObject:
            self.gameObject.Destroy()
