'''
Created on Jan 29, 2014

@author: otrebor
'''
from game.phys import PhysUtility
import Events

class PhysEng:
    
    def __init__(self):
        self.objects = []
        self.toRemove = []
        
    def objCount(self):
        return len(self.objects)
    
    # object is a collider
    def add(self, obj):
        if not(obj in self.objects):
            self.objects.append(obj)
    
    def remove(self, obj):
        self.toRemove.append(obj)
        
    def update(self, delta):
        size = self.objCount()
        for i in range(0, size):
            for j in range(i, size):
                if i != j:  # is not the same
                    self.handleCollision(self.objects[i], self.objects[j])
        self.updateList()
    
    def draw(self, screen):
        for obj in self.objects:
            obj.draw(screen)
    
    def updateList(self):
        for obj in self.toRemove:
            try:
                self.objects.remove(obj)
            except:
                pass
        self.toRemove = []
    
    def handleCollision(self, obj1, obj2):
        dis = 1
        if obj1.isStationary and obj2.isStationary:
            return
        info = PhysUtility.testCollision(obj1, obj2)
        if info != None: 
            if obj1.isTrigger or obj2.isTrigger:
                if obj1.isTrigger and obj2.isTrigger:
                    return
                self.callOnTrigger(obj1,obj2,info)
            else:
                if not obj1.isStationary or not obj2.isStationary:
                    if obj1.isStationary:
                        move = info.direction.scale(info.distance + dis)
                        info.collider2.position = info.collider2.position.add(move.scale(-1))
                    elif obj2.isStationary:
                        move = info.direction.scale(info.distance + dis)
                        info.collider1.position = info.collider1.position.add(move)
                    else:
                        move = info.direction.scale((info.distance + dis) / 2)
                        info.collider1.position = info.collider1.position.add(move)
                        info.collider2.position = info.collider2.position.add(move.scale(-1))
                PhysUtility.HandleCollision(obj1, obj2, info)
                self.callOnCollision(obj1, obj2, info)
    
    '''
    Send message to obj1 and obj2 to call OnCollision
    arg is an object with other (GameObject), normal(Vector2)
    '''
    def callOnCollision(self, obj1, obj2, info):
        coll = Events.OnCollision(obj2.gameObject, info.direction, info.distance)
        coll.CallOn(obj1.gameObject)
        coll = Events.OnCollision(obj1.gameObject, info.direction.scale(-1),info.distance)
        coll.CallOn(obj2.gameObject)
        
    
    def callOnTrigger(self,obj1,obj2,info):
        coll = Events.OnTrigger(obj2.gameObject, info.direction,info.distance)
        coll.CallOn(obj1.gameObject)
        coll = Events.OnTrigger(obj1.gameObject, info.direction.scale(-1),info.distance)
        coll.CallOn(obj2.gameObject)
    

        
