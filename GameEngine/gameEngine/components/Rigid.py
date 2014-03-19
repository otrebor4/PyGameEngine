'''
Created on Jan 28, 2014

@author: otrebor
'''
import gameEngine.components.Component as Component
import gameEngine.util.Vector2 as Vector2


#A rigid gives control of an object's position through physics simulation.
#Must have a collider
class Rigid(Component.Component):
        
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        gameObject.rigid = self
        self.mass = 1.0
        self.velocity = Vector2.Vector2()
        self.applyGravity = True
        self.kinematic = False
        
    # apply movement to object
    def update(self, delta):
        if self.gameObject.collider.isStationary:
            self.velocity = Vector2.Vector2()  # static object can't be moved by given speed must manually change position
        self.gameObject.transform.position = self.gameObject.transform.position.add(self.velocity.scale(delta))
        
        if self.applyGravity:
            grav = self.gameObject.world.gravity
            self.velocity = self.velocity.add(grav.scale(delta))
        
