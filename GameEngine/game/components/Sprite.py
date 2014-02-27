'''
Created on Feb 5, 2014

@author: Otrebor45
'''
import Component
import Render
import game.util.Vector2 as Vector2
import game.Resources as Resources
import game.lib.yaml as yaml
import game.Game

'''
Sprite component, hold and draw image sprite
'''
class Sprite(Render.Render):
    yaml_tag =u'!Sprite'
    def __getstate__(self):
        data = Render.Render.__getstate__(self)
        data['fileName'] = self.fileName
        data['sprite_data'] = self.sprite_data
        data['current'] = self.current
        data['offset'] = self.offset
        return data
    
    def __setstate__(self,state):
        self.__dict__.update(state)
        if game.Game.Game.Instance() and self.fileName:
            g = game.Game.Game.Instance()
            self.image = g.resources.LoadImage(self.fileName)
    
    def __init__(self, gameObject):
        Render.Render.__init__(self, gameObject)
        self.image = None  # sprite image
        self.sprite_data = {}  # a hash as the image name as key, and area (x,y,w,h) as value,
        self.current = ""  # sprite name to use when draw
        self.fileName = ""
        self.offset = (0,0)
        
    def setData(self,fileName, image, sprite_data, current):
        self.fileName = fileName
        self.image = image
        self.sprite_data = sprite_data
        self.current = current
        
    def changeSprite(self, image_name):
        self.current = image_name
    
    def draw(self, screen):
        pos = self.gameObject.shape.StartCorner() if self.gameObject != None and self.gameObject.shape != None else Vector2.Vector2()
        
        
        area = self.sprite_data[self.current] if self.sprite_data.has_key(self.current) else None
        pos = pos.xy()
        pos = (pos[0]+self.offset[0], pos[1]+self.offset[1])
        screen.blit(self.image, pos, area)
        
    def getSprite(self,name):
        area = self.sprite_data[name] if self.sprite_data.has_key(name) else None
        if area:
            img = game.Game.pygame.Surface( (area[2],area[3]), pygame.SRCALPHA, 32)
            img.fill( (0,0,0,0))
            img.blit(self.image,(0,0), area)
            return img
        return self.image
    
'''
Component that animate sprite on a gameObject
'''
class SpriteAnim(Component.Component):
    yaml_tag = u'!SpriteAnim'
    def __getstate__(self):
        data = Component.Component.__getstate__(self)
        data['sprite'] = self.sprite
        data['animations'] = self.animations
        data['current_animation'] = self.current_animation
        data['speed'] = self.speed
        return data
        
    def __init__(self, gameObject):
        Component.Component.__init__(self, gameObject)
        self.sprite = self.gameObject.getComponent("Sprite")
        self.animations = {}  # animation data, animation_name(string) :Value Animation()
        self.current_animation = "anim1"  # animation name to play
        self.speed = 1.0
    
    def setAnimations(self,animations):
        self.animations = animations
    
    def setSpeed(self, newSpeed):
        self.speed = newSpeed
    
    def play(self, name, speed=1):
        self.current_animation = name
        self.speed = speed
    
    def update(self, delta):
        if self.current_animation == 'default' and len(self.animations.keys()) > 0:
            self.current_animation = self.animations.keys()[0]
        
        if self.animations.has_key(self.current_animation):
            animData = self.animations[self.current_animation]
            animData.update(delta * self.speed)
            self.sprite.changeSprite(animData.currentFrame())
        
  
class Animation(yaml.YAMLObject):
    yaml_tag =u'!Animation'
    
    def __getstate__(self):
        data = {}
        data['name'] = self.name
        data['speed'] = self.speed
        data['frames'] = self.frames
        data['current_frame'] = self.current_frame
        return data
    
    def __init__(self, name="None", speed=1, frames=[]):
        self.name = name
        self.speed = speed  # currently time to change_to_next frame
        self.frames = frames
        self.current_frame = 0
        self.timer = 0
        
    def currentFrame(self):
        if self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None
    
    # function to update animation frame,
    
    def update(self, delta):
        self.timer += delta
        if self.timer >= self.speed:
            flen = len(self.frames)
            self.current_frame = (self.current_frame + 1) % flen
            self.timer = 0



def AddSprite(gameObject,file_name, resources=Resources.Resources(""), offset = (0,0), img_name = None):
    (fileName,image,spritedata,anim) = loadData(file_name,resources)
    sprite = gameObject.addComponent(Sprite)
    if not img_name:
        img_name = spritedata.keys()[0]
    sprite.setData(fileName,image,spritedata, img_name)
    sprite.offset = offset
    
    
def AddAnimator(gameObject,file_name,resources=Resources.Resources(""),offset = (0,0),img_name=None):
    (fileName,image,spritedata,anims) = loadData(file_name,resources)
    sprite = gameObject.addComponent(Sprite)
    if not img_name:
        img_name = spritedata.keys()[0]
    sprite.setData(fileName,image,spritedata,img_name)
    sprite.offset = offset
    anims = makeAnimations(anims)
    spriteAnim = gameObject.addComponent(SpriteAnim)
    spriteAnim.setAnimations(anims)
    return spriteAnim
    
    
def makeAnimations(anims):
    animations = {}
    for k in anims.keys():
        animations[k] = Animation(k,1,anims[k])
    return animations


def loadData(file_name, resources=Resources.Resources("")):
    spritedata = {}
    anims = {}
    f = open(file_name)
    image_name = f.readline().rstrip('\n')  # first line is the image_directory
    #image_name.
    for line in f:
        if '@' in line:
            (name, data) = parseAnimationline(line)
            anims[name] = data
        else:
            (sname, (x, y, w, h)) = parseSpriteLine(line)
            spritedata[sname] = (x, y, w, h)
    image = resources.LoadImage(image_name)
    return (image_name,image, spritedata, anims)

'''
pares animation sprite data,
format:
@name:sp1,sp2,sp3
'''   
def parseAnimationline(line):
    line = line.rstrip()
    line = line.replace('@','')
    (name, (sprites)) = line.split(":")
    images = []
    for sn in sprites.split(','):
        images.append(sn)
    return (name, images)
    
'''
parse image sprite data, string
format:
name:x,y,w,h
'''
def parseSpriteLine(line):
    (name, data) = line.split(":")
    (x, y, w, h) = data.split(",")
    return (name, (int(x), int(y), int(w), int(h))) 
        


import pygame    
if __name__ == '__main__':
    #pygame.init()
    #screen = pygame.display.set_mode((150,150))
    _game = game.Game.Game()
    obj = _game.world.createObject()
    sprite = obj.addComponent(Sprite)
    data = loadData('Resources/sprites/anim1.txt', Resources.Resources("Resources/"))
    sprite.setData(data[0], data[1],data[2], "no")
    f = yaml.dump(sprite) #, stream, Dumper)
    o = yaml.load(f)#, Loader)
    
    
    pass
        
        
        

        
        
        
        
        
        
