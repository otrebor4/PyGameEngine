'''
Created on Mar 5, 2014

@author: rfloresx
'''
import game.components.Component as Component
import game.util.Vector2 as Vector2
import pygame


class Controller(Component.Component):
    
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.coldown = 0
        if self.gameObject.rigid:
            self.gameObject.rigid.kinematic = True
        self.walkSpeed = 100
        self.runSpeed = self.walkSpeed * 2
        
    def update(self, delta):
        self.coldown -= delta
        speed = self.walkSpeed
        if self.coldown <= 0:
            self.coldown += .01
            vel = Vector2.Vector2()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_k]:
                speed = self.runSpeed
            if keys[pygame.K_w]:
                vel = vel.add(Vector2.Vector2(0, -1))
            if keys[pygame.K_s]:
                vel = vel.add(Vector2.Vector2(0, 1))
            if keys[pygame.K_a]:
                vel = vel.add(Vector2.Vector2(-1, 0))
            if keys[pygame.K_d]:
                vel = vel.add(Vector2.Vector2(1, 0))
            if self.gameObject.rigid:
                vel =  lerp(self.gameObject.rigid.velocity,vel.normalize().scale(speed),6*delta)
                vel = vel if vel.magnitude() > .01 else Vector2.Vector2()
                self.gameObject.rigid.velocity = vel

class FlashLightController(Component.Component):
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        pass
    def update(self,delta):
        rigid = self.gameObject.rigid
        light = self.gameObject.getComponent('FlashLight')
        if rigid:
            speed = rigid.velocity.magnitude() *1
            angle = rigid.velocity.angle()
            if speed < 1: #no moving
                return
            light.angle = angle

class Rotate(Component.Component):
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.angle = 0
    
    def update(self,delta):
        self.angle += delta * 100
        self.transform.rotation = self.angle
        
def lerp(start,end,lval):
    mid = end.sub(start)
    mid = mid.scale(lval)
    return start.add(mid)