'''
Created on Mar 5, 2014

@author: rfloresx
'''
import gameEngine.Game as game
import gameEngine.util.Vector2 as Vector2
from scripts import Sample
import gameEngine.components.LightSource as LightSource

class Main(game.Game):
    def __init__(self):
        game.Game.__init__(self)
        self.DEBUG = True
        #self.world.addObject(self.circle())
        self.world.addObject(self.testCircle((255,255), 10))
        self.world.addObject(self.testRect((500,500), (100,100)))
        self.world.addObject(self.testRect((255,500), (100,100)))
        self.world.addObject(self.light( ))
        self.addTest2Objects((0, 0), 50, (50, 50))
        #self.world.setLight( (255,255,255,255))
        
    def addTest2Objects(self, (x,y), r, (w,h)):
        parent = self.world.createCircGameObject(x, y, r, True, False)
        parent.name = "parent"
        parent.addComponent(Sample.Controller)
        rot = parent.addComponent(Sample.Rotate)
        rot.speed = 20
        self.world.addObject(parent)
        child = self.world.createRectGameObject(0, 0, w, h, True, False)
        child.transform.parent = parent.transform
        child.transform.localPosition = Vector2.Vector2(4*r, 0)
        child.name = "child"
        rot = child.addComponent(Sample.Rotate)
        rot.speed = 200
        self.world.addObject(child)
        child2 = self.world.createRectGameObject(0, 0, w, h, True, False)
        child2.transform.parent = child.transform
        child2.transform.localPosition = Vector2.Vector2(2*r, 0)
        child2.name = "child2"
        rot = child2.addComponent(Sample.Rotate)
        rot.speed = 50
        self.world.addObject(child2)
        return parent
        
        
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