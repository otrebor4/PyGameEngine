'''
Created on Feb 3, 2014

@author: rfloresx
'''
import pygame

class Resources:
    def __init__(self, folder="Resources/"):
        self.LoadedResources = {}
        self.dir = folder
        
    def ClearLoaded(self):
        self.LoadedResources = {}
    
    # current only load image
    
    def LoadImage(self, key):
        skey = self.dir + key
        skey = skey.strip()
        if self.LoadedResources.has_key(skey):
            return self.LoadedResources[skey]
        else:
            img = pygame.image.load(skey).convert_alpha()
            self.LoadedResources[skey] = img
            return img
    
