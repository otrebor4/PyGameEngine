'''
Created on Jan 27, 2014

@author: otrebor
'''
import game.components.Sprite
import game.base.CircleObject as CircleObject
import game.base.RectObject as RectObject
import phys.PhysEng as PhysEng
import game.components.Rigid as Rigid
import util.Vector2 as Vector2
import Terrain
import game.base.GameObject as GameObject
import game.components.Collider as Collider
import game.phys.shapes.Polygon as Polygon
import game.lib.yaml as yaml

#world is the area for all objects
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
    
    #save terrain to text file  
    def saveTerrain(self,fileName):
        with open(fileName, 'w') as outfile:
            yaml.dump(self.terrain,outfile)
    
    #loads terrain from text file
    def loadTerrain(self,map_file,objs):
        self.map_file = map_file
        self.objs = objs
        self.load = True
    
    #calls reset, cleans up world
    def resetWorld(self):
        self.reset = True
    
    #load entire world with all maps and objects
    def loadWorld(self, objs, files):
        self.load = True
        self.objs = objs
        self.layers = files
        
    '''
    GameObject loading
    '''
    def createObject(self):
        obj = GameObject.GameObject(self)
        return obj
    
    def createPolygon(self, points, static=True):
        obj = GameObject.GameObject(self)
        ((x, y), vectors) = Polygon.getPolygonFromPoints(points)
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
            cir.addComponent(Rigid.Rigid)
        self.phyEng.add(cir.collider)
        self.objects.append(cir)
        return cir
    
    def createRect(self, x, y, w, h, color=(0, 0, 0), riged=True):
        r = RectObject.RectObject(self, x, y, w, h, color)
        if riged:
            r.addComponent(Rigid.Rigid)
        self.addObject(r)
        return r
    
    def createSprite(self,x,y,w,h, sprite_data,animations=False,riged = True):
        r = RectObject.RectObject(self, x, y, w, h)
        if riged:
            r.addComponent(Rigid.Rigid)
            if animations:
                game.components.Sprite.addAnimator(r, sprite_data, self.main.resources)
            else:
                game.components.Sprite.addSprite(r, sprite_data, self.main.resources)
        self.addObject(r)
        return r
    
    def createRectGameObject(self,x,y,w,h,riged = True,trigger = False):
        obj = GameObject.GameObject(self)
        col = Collider.RectCollider(obj, x, y, w, h)
        col.isTrigger = trigger
        if riged:
            obj.addComponent(Rigid.Rigid)
        self.addObject(obj)
        return obj
    def createCircGameObject(self,x,y,r,riged = True, trigger = False):
        obj = GameObject.GameObject(self)
        col = Collider.CircleCollider(obj,x,y,r)
        col.isTrigger = trigger
        if riged:
            obj.addComponent(Rigid.Rigid)
        self.addObject(obj)
        return obj

    '''
    GameObject retriver
    '''
    #retrieves object from world
    def findObject(self,name):
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None
    
    #returns first object within a circle with radius (distance), and center (x,y)
    def getFirstRange(self, (x,y), distance):
        for obj in self.objects:
            if obj.shape and obj.shape.position.distance(Vector2.Vector2(x,y)) <= distance:
                return obj
        return None
    
    #return all objects within a circle with radius (distance), and center (x,y)
    def getOnRange(self, (x,y), distance, filters = {}):
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

    def addObject(self, gameObject):
        if not gameObject:
            return
        if not (gameObject in self.objects):
            self.objects.append(gameObject)
        if gameObject.collider:
            self.phyEng.add(gameObject.collider)
    
    def delete(self, gameObject):
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
            except:
                pass
        self.toRemove = []
        if self.reset:
            self.reset()
            self.reset = False
        if self.load:
            self.load = False
            self.load()
            
    def reset(self):
        self.phyEng.objects = []
        self.objects = []
        self.terrain.layers = []
        self.main.reset()
        
    def load(self):
        self.reset()
        data = {}
        if self.map_file:
            data  = self.terrain.makeTerrain(self.map_file)
        for obj in self.objs:
            self.addObject(obj)
        data["objects"] = self.objects
        self.main.load(data)
        
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
            
        
