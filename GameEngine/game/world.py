'''
Created on Jan 27, 2014

@author: otrebor
'''
import game.components.Sprite as Sprite
import game.base.CircleObject as CircleObject
import game.base.RectObject as RectObject
import phys.PhysEng as PhysEng
import components.Riged as Riged
import util.Vector2 as Vector2
import Terrain
import game.base.GameObject as GameObject
import game.components.Collider as Collider
import game.phys.shapes.Polygon as Polygon
import game.lib.yaml as yaml

class World:
    
    
    
    def __init__(self, main, size, gravity=Vector2.Vector2()):
        size = (main.screen.get_width(), main.screen.get_height())
        self.terrain = Terrain.Terrain(main.resources, size, self)
        self.phyEng = PhysEng.PhysEng()
        self.objects = []
        self.toRemove = []
        self.gravity = gravity
        self.main = main
        self.reset = False
        self.load = False
        self.objs = []
        self.map_file = []
        self.name = "world"
        self.music = []
        self.size = size
    '''
    Terrain loading 
    '''
      
    def saveTerrain(self,fileName):
        with open(fileName, 'w') as outfile:
            yaml.dump(self.terrain,outfile)
        #yaml.sa
          
    def LoadTerrain(self,map_file,objs):
        self.map_file = map_file
        self.objs = objs
        self.load = True
    
    def resetWorld(self):
        self.reset = True
    
    def loadWorld(self, objs, files):
        self.load = True
        self.objs = objs
        self.layers = files
        
    '''
    GameObject loading
    '''
    def createObject(self):
        obj = GameObject.GameObject(self)
        #self.AddObject(obj)
        return obj
    
    def createPolygon(self, points, static=True):
        obj = GameObject.GameObject(self)
        ((x, y), vectors) = Polygon.getPoligonFromPoints(points)
        obj.collider = Collider.PolygonCollider(obj, x, y, vectors)
        self.phyEng.add(obj.collider)
        obj.collider.static = static
        self.objects.append(obj)
        return obj
        
    def createWall(self, x, y, w, h, color=(0, 0, 0)):
        wall = RectObject.RectObject(self, x, y, w, h, color)
        self.phyEng.add(wall.collider)
        wall.collider.static = True
        wall.collider.isTrigger = True
        self.objects.append(wall)
        return wall
    
    def createCircle(self, x, y, r, color=(0, 0, 0), riged=True):
        cir = CircleObject.CircleObject(self, x, y, r, color)
        if riged:
            cir.addComponent(Riged.Riged)
        self.phyEng.add(cir.collider)
        self.objects.append(cir)
        
        return cir
    
    def createRect(self, x, y, w, h, color=(0, 0, 0), riged=True):
        r = RectObject.RectObject(self, x, y, w, h, color)
        if riged:
            r.addComponent(Riged.Riged)
        
        self.AddObject(r)
        return r
    
    def createSprite(self,x,y,w,h, sprite_data,animations=False,riged = True):
        r = RectObject.RectObject(self, x, y, w, h)
        if riged:
            r.addComponent(Riged.Riged)
            if animations:
                Sprite.AddAnimator(r, sprite_data, self.main.resources)
            else:
                Sprite.AddSprite(r, sprite_data, self.main.resources)
        self.AddObject(r)
        return r
    
    def createRectGameObject(self,x,y,w,h,riged = True,trigger = False):
        obj = GameObject.GameObject(self)
        col = Collider.RectCollider(obj, x, y, w, h)
        col.isTrigger = trigger
        if riged:
            obj.addComponent(Riged.Riged)
        self.AddObject(obj)
        return obj
    def createCircGameObject(self,x,y,r,riged = True, trigger = False):
        obj = GameObject.GameObject(self)
        col = Collider.CircleCollider(obj,x,y,r)
        col.isTrigger = trigger
        if riged:
            obj.addComponent(Riged.Riged)
        self.AddObject(obj)
        return obj
    '''
    GameObject retriver
    '''
    def FindObject(self,name):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None
    
    def GetFirstRange(self, (x,y), distance):
        for obj in self.objects:
            if obj.shape and obj.shape.position.distance(Vector2.Vector2(x,y)) <= distance:
                return obj
        return None
    
    def GetOnRange(self, (x,y), distance, filters = {}):
        objs = []
        pos = Vector2.Vector2(x,y)
        for obj in self.objects:
            if obj.shape and pos.distance(obj.shape.position) <= distance:
                if len(filters):
                    for n in filters:
                        if n in obj.name:
                            objs.append(obj)
                else:
                    objs.append(obj)
        return objs
    
    def validatePosition(self, (x,y)):
        (w,h) = self.size
        return x > 0 and x < w and y > 0 and y < h
    
    '''
    '''
    def AddObject(self, gameObject):
        if not gameObject:
            return
        if not (gameObject in self.objects):
            self.objects.append(gameObject)
        if gameObject.collider:
            self.phyEng.add(gameObject.collider)
    
    def Delete(self, gameObject):
        self.phyEng.remove(gameObject.collider)
        self.toRemove.append(gameObject)
        
    def update(self, delta):
        # update game logic
        for obj in self.objects:
            obj.update(delta)
        # update physics
        self.phyEng.update(delta)
        self.updateRemove()
    
    def updateRemove(self):
        for obj in self.toRemove:
            try:
                self.objects.remove(obj)
                #obj.sendMessage("OnDestroy")
            except:
                pass
        self.toRemove = []
        if self.reset:
            self.reset()
            self.reset = False
        if self.load:
            self.load = False
            self.Load()
            
    def Reset(self):
        self.phyEng.objects = []
        self.objects = []
        self.terrain.layers = []
        self.main.Reset()
        
    def Load(self):
        self.Reset()
        data = {}
        if self.map_file:
            data  = self.terrain.MakeTerrain(self.map_file)
        for obj in self.objs:
            self.AddObject(obj)
        data["objects"] = self.objects
        self.main.Load(data)
        
    def debDraw(self, screen):
        self.phyEng.draw(screen)
        self.terrain.navMesh.print_graph(screen,(0,255,0))
        
    def draw(self, screen):
        # call draw
        # draw first and second layer
        self.terrain.drawLayer(screen, (0, 1))
        for obj in self.objects:
            obj.draw(screen)
        self.terrain.drawLayer(screen, (2, 3))
        self.terrain.drawMask(screen)
    
    def OnGUI(self,screen):
        for obj in self.objects:
            obj.OnGUI(screen)
            
    def broadcast(self, func, arg ):
        for obj in self.objects:
            obj.sendMessage(func, arg )
            
        
