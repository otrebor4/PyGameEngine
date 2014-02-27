'''
Created on Feb 3, 2014

@author: rfloresx
'''
import pygame
import Resources
import game.components.Collider as Collider
import base.GameObject as GameObject
import game.phys.physutil as util
import game.util.Vector2 as Vector2
import util.graph as graph
import game.lib.yaml as yaml
import scripts.CreateMap as CreateMap
import game.components.LightSource as LightSource
import game.util.NavMesh as NavMesh


class TyleInfo:
    def __init__(self, pos, area=None, data = {'image':None,'name':''}):
        self.pos = pos
        self.area = area
        self.data = data
        self.image = data['image']
        
        
    def rect(self):
        (w, h) = (self.area[2], self.area[3]) if self.area != None else (64, 64)
        return (self.pos[0], self.pos[1], w, h)
    
    
class Terrain(yaml.YAMLObject):
    yaml_tag = u'!Terrain'
    
    def __getstate__(self):
        data = {}
        data['navMesh'] = self.navMesh 
        
        return data
    
    def __init__(self, resources=Resources.Resources(), size=(512, 512), world=None, color = (255,255,255,255)):
        self.size = size
        self.layers = []
        self.resources = resources
        self.world = world
        self.mask = pygame.Surface([size[0], size[1]], pygame.SRCALPHA, 32).convert_alpha()
        self.mask.fill(color)
        self.original = self.mask.copy()
        self.haveLight = False
        self.navMesh = NavMesh.NavMesh()
        #self.mask = self.mask.convert_alpha()
        
    def GenerateLayer(self, tyles):
        width = self.size[0]
        height = self.size[1]
        layer = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        layer = layer.convert_alpha()  # create layer of the size of the screen
        
        # layer.fill( (0,0,0,0))#clear layer
        for tyle in tyles:
            layer.blit(tyle.image, tyle.pos, tyle.area)
        return layer.convert_alpha()
    
    def makeData(self, line):
        data = {}
        line = line.strip()
        tokens = line.split(',')
        if '.png' in tokens[0]:
            data['image'] = self.resources.LoadImage(tokens[0])
        for i in range(1,len(tokens)):
            token = tokens[i]
            if ':' in token:
                tks = token.split(':')
                key = tks[0]
                val = tks[1]
            else:
                key = token
                val = True
            data[key] = val
        return data
    '''
    load layer from file, if haveCollision will return a list of collider objects
    '''
    def MakeTerrain(self, map_file): 
        setAttr = False
        size = 64
        tyles = None
        data = {}
        nav = None
        mesh = False
        with open(map_file) as f:
            y = 0;
            for line in f:
                line = line.strip()
                if ':' in line:#is key:image
                    line = line.strip()
                    cmap = line.split(':', 1)                    
                    if ".png" in cmap[1]: #well seems  to be tyle data
                        data[cmap[0]] = self.makeData(cmap[1])
                        if not 'name' in data[cmap[0]].keys():
                            data[cmap[0]]['name'] = cmap[0]
                    else:
                        data[cmap[0]] = cmap[1]
                elif '@' in line:#world start
                    if tyles:#check if interrupt layer, save layer
                        self.layers.append(self.GenerateLayer(tyles))
                        if setAttr:
                            self.LoadAttributes(tyles,data)
                    if nav and mesh:
                            self.LoadNav(nav)
                    nav = None
                    tyles = None
                    setAttr = "True" in line
                    mesh = "Navmesh" in line
                    y = 0
                else:
                    if not nav:
                        nav = []
                    if tyles == None:
                        tyles = []
                    x = 0;
                    line = line.strip()
                    for c in line:
                        if mesh:
                            if c == 'M':
                                nav.append(TyleInfo( (x,y), (0,0,size,size) ))
                        elif data.has_key(c):
                            tyles.append(TyleInfo((x, y), (0, 0, size, size), data[c] ))
                        
                            
                        x = x + size
                    y = y + size
            if tyles:#check if there left over tyles
                self.layers.append(self.GenerateLayer(tyles))
                if setAttr:
                    self.LoadAttributes(tyles,data)
            if mesh and nav:
                self.LoadNav(nav)
                    
        return data
    
    '''
    Create colliders to tyles
    '''
    def LoadNav(self,nav):
        #print "nav"
        navMesh = NavMesh.NavMesh()
        for tyle in nav:
            (x,y,w,h) = tyle.rect()
            p0 = (x,y)
            p1 = (x+w,y)
            p2 = (x+w,y+h)
            p3 = (x,y+h)
            navMesh.addEdge(p0,p1)
            navMesh.addEdge(p1,p2)
            navMesh.addEdge(p2,p3)
            navMesh.addEdge(p3,p0)
        self.navMesh = navMesh.makeNavMesh()
        #self.navMesh.print_graph()
        #pygame.time.wait(1000)
    
    def LoadAttributes(self,tyles,data):
        #print "attr"
        graphs = {}
        for tyle in tyles:
            name = tyle.data['name']
            if not name in graphs:
                graphs[name]= graph.Graph()
            (x,y,w,h) = tyle.rect()
            p0 = (x,y)
            p1 = (x+w,y)
            p2 = (x+w,y+h)
            p3 = (x,y+h)
            graphs[name].addEdge(p0,p1)
            graphs[name].addEdge(p1,p2)
            graphs[name].addEdge(p2,p3)
            graphs[name].addEdge(p3,p0)
            
        for key in graphs.keys():
            info = {}
            info = data[key]
            g = graphs[key]
            
            cs = g.getCicles()
            for poly in cs:
                block = GameObject.GameObject(self.world)
                block.collider = Collider.PolygonCollider(block, 0, 0, self.toVector2(poly) )
                self.world.AddObject(block)
                if 'static' in info.keys():
                    block.collider.static = info['static']
                if 'trigger' in info.keys():
                    block.collider.isTrigger = info['trigger']
                if 'light' in info.keys():
                    light = block.addComponent(LightSource.SpotLight)
                    if 'intensity' in info.keys():
                        light.intensity = int(info['intensity'])
                    if 'radius' in info.keys():
                        light.radius = int(info['radius'])
                        
                if 'sink' in info.keys():
                    sink = block.addComponent(CreateMap.Sink)
                    if 'damage' in info.keys():
                        sink.damage = float(info['damage'])
                elif 'damage' in info.keys():
                    damage = block.addComponent(CreateMap.Damage)
                    damage.damage = float(info['damage'])    
                elif 'goal' in info.keys():
                    block.addComponent(CreateMap.Goal)
                    
                    
    def toVector2(self, poly):
        _list = []
        for i in range(0, len(poly)):
            _list.append( Vector2.Vector2(poly[i][0], poly[i][1]))
            
        
        return _list
    
    def drawLayer(self, screen, args):
        for arg in args:
            if arg < len(self.layers):
                screen.blit(self.layers[arg], (0, 0))
    
    def makeMask(self,orig):
        temp = orig.copy()
        temp.fill( (255,255,255,255))
        temp.blit(orig,(0,0), special_flags = pygame.BLEND_RGB_SUB)
        return temp.convert_alpha()
        
    
    def drawMask(self,screen):
        if not self.haveLight:
            self.mask.fill((0,0,0,225))
        screen.blit(self.mask,(0,0))
        self.mask = self.original.copy()
        self.haveLight = False
    
    def AddLight(self,ligthMask, pos):
        self.mask.blit(ligthMask,pos, special_flags = pygame.BLEND_RGBA_MULT)
        self.haveLight = True
    
    def GetPath(self, start, goal):
        if self.navMesh.data:
            return self.navMesh.GetPath(Vector2.Vector2(*start), Vector2.Vector2(*goal))
        return None
                
    def validPosition(self, pos):
        if self.navMesh.data:
            return self.navMesh.data.get_node_from_point(Vector2.Vector2(*pos)) != None 
        return None   
