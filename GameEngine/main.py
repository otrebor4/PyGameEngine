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
        self.DEBUG = True
        #self.world.addObject(self.circle())
        #self.world.addObject(self.testCircle((255,255), 10))
        self.world.addObject(self.testRect((500,500), (100,100)))
        #self.world.addObject(self.testRect((255,500), (100,100)))
        self.world.addObject(self.light( ))
        
        #self.world.setLight( (255,255,255,255))
        
    def testCircle(self, (x,y), r):
        obj = self.world.createCircGameObject(x, y, r, True, False)
        obj.name = "testC"
        return obj
    def testRect(self, (x,y), (w,h)):
        obj = self.world.createRectGameObject(x, y, w, h, True, False)
        obj.name = "testC"
        obj.addComponent(Sample.Rotate)
        return obj
    
    def light(self):
        light = self.world.createObject()
        l = light.addComponent(LightSource.EnvironmentLight)
        l.setVal( (255,255,255,255) )
        return light
    
    def circle(self):
        circle = self.world.createCircle(500, 500, 50, (255,255,255),True)
        circle.name = 'player'
        circle.rigid.velocity = Vector2.Vector2(0,100)
        circle.addComponent(Sample.Controller)
        #flashLight = circle.addComponent(LightSource.FlashLight)
        #flashLight.setVals(350,250,180,(255,0,0),20, (0,0))
        #circle.addComponent(Sample.FlashLightController)
        
        return circle
        
if __name__ == '__main__':
    m = Main()
    m.run()