'''
Created on Jan 28, 2014

@author: otrebor
'''
import pygame

import GameObject
import game.components.Render as Render
import game.components.Collider as Collider
import game.util.Vector2 as Vector2

#creates game object of circle type
class CircleObject(GameObject.GameObject):
    def __init__(self, world, x, y, r, color):
        GameObject.GameObject.__init__(self, world)
        self.transform.position = Vector2.Vector2( x,y)
        Collider.CircleCollider(self, 0, 0, r)
        render = self.addComponent(CircleRender)
        render.color = color
        render.radius = r
        
class CircleRender(Render.Render):    
    def __init__(self, gameObject):
        Render.Render.__init__(self, gameObject)
        self.color = (0,0,0,0)
        self.radius = 0
        self.offset = Vector2.Vector2(0,0)
        
    @property
    def center(self):
        return self.transform.position.add( self.offset).xy()
        
    def draw(self, screen):
        center = self.center
        pygame.draw.circle(screen, self.color, ( int(center[0]), int(center[1])), self.radius)
        
        
