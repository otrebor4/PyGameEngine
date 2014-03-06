'''
Created on Mar 5, 2014

@author: rfloresx
'''
import game.Game as game
import game.util.Vector2 as Vector2
from scripts import Sample
import game.components.LightSource as LightSource

class Main(game.Game):
    def __init__(self):
        game.Game.__init__(self)
        self.world.addObject(self.circle())
        
    def circle(self):
        circle = self.world.createCircle(255, 255, 50, (255,255,255),True)
        circle.rigid.velocity = Vector2.Vector2(0,100)
        circle.addComponent(Sample.Controller)
        flashLight = circle.addComponent(LightSource.FlashLight)
        flashLight.setVals(350,250,180,(255,0,0),20, (0,0))
        circle.addComponent(Sample.FlashLightController)
        
        return circle
        
if __name__ == '__main__':
    m = Main()
    m.run()