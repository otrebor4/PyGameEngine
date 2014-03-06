'''
Created on Jan 28, 2014

@author: otrebor
'''
import game.lib.yaml as yaml

#Base class for a component
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
    
    def rigid(self):
        if self.gameObject:
            return self.gameObject.rigid
        return None