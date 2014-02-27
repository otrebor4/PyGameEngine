'''
Created on Jan 28, 2014

@author: otrebor
'''
import pygame

import GameObject
import game.components.Collider as Collider
import game.components.Render as Render

class RectObject(GameObject.GameObject):
    yaml_tag = u'!RectObject'
    def __init__(self, world, x, y, w, h, color=None):
        GameObject.GameObject.__init__(self, world)
        
        Collider.RectCollider(self, x, y, w, h)
        render = self.addComponent(RectRender)
        render.color = color
                
class RectRender(Render.Render):
    yaml_tag = u'!RectRender'
    def __getstate__(self):
        data = Render.Render.__getstate__(self)
        data['color'] = self.color
        return data
    
    def __init__(self, gameObject):
        Render.Render.__init__(self, gameObject)
        self.color = (0,0,0,0)
        
    def rect(self):
        x = self.gameObject.shape.Left()
        y = self.gameObject.shape.Top()
        w = self.gameObject.shape.Width()
        h = self.gameObject.shape.Height()
        return pygame.rect.Rect(x, y, w, h)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect())
        
