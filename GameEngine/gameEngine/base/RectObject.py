'''
Created on Jan 28, 2014

@author: otrebor
'''
import pygame

import GameObject
import gameEngine.components.Collider as Collider
import gameEngine.components.Render as Render
import gameEngine.util.Vector2 as Vector2
#creates game object of rectangle type
class RectObject(GameObject.GameObject):
    def __init__(self, world, (x, y)=(0,0), (w, h)=(0,0), color=None):
        GameObject.GameObject.__init__(self, world)
        Collider.RectCollider(self, (0,0), w, h)
        render = self.addComponent(RectRender)
        render.color = color
        self.transform.position = Vector2.Vector2(x,y)
        
class RectRender(Render.Render):
    
    def __init__(self, gameObject):
        Render.Render.__init__(self, gameObject)
        self.color = (0,0,0,0)
        self.offset = (0,0)
    def rect(self):
        x = self.shape.left     + self.offset[0]
        y = self.shape.top      + self.offset[1]
        w = self.shape.width    + self.offset[0]
        h = self.shape.height   + self.offset[1]
        return pygame.rect.Rect(x, y, w, h)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect())
        
