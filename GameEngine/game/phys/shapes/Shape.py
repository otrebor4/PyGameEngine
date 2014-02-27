'''
Created on Jan 28, 2014

@author: otrebor
'''
import math

import game.util.Vector2 as Vector2
import pygame
import game.lib.yaml as yaml

class Shape(yaml.YAMLObject):
    yaml_tag = u'!Shape'
    def __getstate__(self):
        data = {}
        data['position'] = self.position
        data['aabb'] = self.aabb
        return data
    
    def __init__(self, x, y):
        self.position = Vector2.Vector2(x, y)
        self.aabb = (0, 0, 0, 0)
    
    '''
    =========AABB useful variables
    '''
    
    def calAABB(self):
        return (self.Left(), self.Top(), self.Right(), self.Bottom())
    
    def Left(self):
        return self.aabb[0] + self.position.x
    def Top(self):
        return self.aabb[1] + self.position.y
    
    def Right(self):
        return self.aabb[2] + self.position.x
    
    def Bottom(self):
        return self.aabb[3] + self.position.y
    
    
    
    def Width(self):
        return self.Right() - self.Left()
    
    def Height(self):
        return self.Bottom() - self.Top()
    
    def Center(self):
        x = self.Left() + self.Width() / 2
        y = self.Top() + self.Height() / 2
        return Vector2.Vector2(x, y)
    
    def StartCorner(self):
        x = self.Left()
        y = self.Top()
        return Vector2.Vector2(x,y)
        
    
    def Radius(self):
        w = self.Width()
        h = self.Height()
        
        return math.sqrt(w * w + h * h)
    
    def draw(self, screen):
        s = pygame.Surface([self.Width(), self.Height()], pygame.SRCALPHA, 32)
        s.fill((250, 0, 0, 100))
        
        screen.blit(s, (self.Left(), self.Top()))
        pass
    
    def Points(self):
        points = [(self.Left(),self.Top()), 
                  (self.Right(),self.Top()),
                  (self.Right(),self.Bottom()),
                  (self.Left(),self.Bottom())]
        return points
        
            
            