'''
Created on Jan 28, 2014

@author: otrebor
'''
import pygame

import GameObject
import game.components.Render as Render
import game.components.Collider as Collider


class CircleObject(GameObject.GameObject):
    yaml_tag = u'!CircleObject'
    def __init__(self, world, x, y, r, collor):
        GameObject.GameObject.__init__(self, world)
        Collider.CircleCollider(self, x, y, r)
        render = self.addComponent(CircleRender)
        render.color = collor
        
class CircleRender(Render.Render):
    yaml_tag = u'!CircleRender'
    def __getstate__(self):
        data = Render.Render.__getstate__(self)
        data['color'] = self.color
        return data
    
    def __init__(self, gameObject):
        Render.Render.__init__(self, gameObject)
        self.color = (0,0,0,0)
        
        
    def draw(self, screen):
        pos = self.gameObject.shape.position
        pygame.draw.circle(screen, self.color, (int(pos.x), int(pos.y)), int(self.gameObject.shape.radius))
        
        
        
        
        
        
