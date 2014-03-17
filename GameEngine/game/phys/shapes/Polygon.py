'''
Created on Jan 28, 2014

@author: otrebor
'''
'''
points are not world points is a set of vectors using x,y as reference point, to simplify movement
'''
import Shape
import game.util.Vector2 as Vector2
import pygame

class Polygon(Shape.Shape):
    def __init__(self,transform, (x,y) = (0,0), points = [], angle = 0):
        Shape.Shape.__init__(self, transform)
        self._angle = angle
        self._offset = (x,y)
        self._corners = [ Vector2.Vector2(pt.x, pt.y) for pt in points ]
        self._cache = None
        self._cachePos = Vector2.Zero
        self.calAABB()
        
    def calAABB(self):
        self.aabb = (min([pt.x for pt in self.corners]),
                     min([pt.y for pt in self.corners]),
                     max([pt.x for pt in self.corners]),
                     max([pt.y for pt in self.corners]))
        return self.aabb
    
    @property
    def corners(self):
        if self._cache:
            if self._cachePos != self.center:
                offset = self.center.sub(self._cachePos)
                self._cachePos = self.center
                offset = offset.rotate(self.transform.localRotation)
                for i in range(0, len(self._cache)):
                    self._cache[i] = self._cache[i].add(offset)
            return self._cache
        
        self._cache = []
        for point in self._corners:
            self._cache.append(point.rotate(self.angle).add(self.center).rotate(self.transform.localRotation))
        self._cachePos = self.center
        return self._cache
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self,value):
        if self._angle != value:
            self._cache = None
            self._angle = value
            self.calAABB()
        
    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self,value):
        if self._offset != value:
            self._offset = value
            self._cache = None
            self.calAABB()
            
    @property
    def center(self):
        return self.transform.position.add(Vector2.Vector2(*self.offset))
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self,value):
        self._radius = value
        self.calAABB()
    
    @property
    def pointlist(self):
        pl = []
        for p in self.points:
            pl.append(p.xy())
        return pl
    @property
    def points(self):
        points = []
        for i in range(0, len(self.corners)):
            points.append(self.corners[i])
        return points
    
    def draw(self, screen):
        color = (255,0,0,100)
        pygame.draw.polygon(screen, color, self.pointlist)
        self.drawaabb(screen)
        
    def drawaabb(self,screen):
        color = (0,255,0,100)
        self.calAABB()
        pos = self.startCorner
        pygame.draw.rect(screen, color,  (int(pos.x),int(pos.y), int(self.width), int(self.height)) )
        
    def getEdges(self):
        edges = []
        corners = self.corners
        for i in range(0, len(corners)):
            edges.append((corners[i - 1], corners[i]))
        return edges
    
    '''  
    def rotate(self,angle):
        corners = []
        for point in self.corners:
            corners.append(point.rotate(angle))
        return Polygon(self.position.x, self.position.y, corners )
    
    def getEdges(self):
        # get all edges on polygon
        # edges are correct world position
        edges = []
        for i in range(0, len(self.corners)):
            edges.append((self.corners[i - 1].add(self.position), self.corners[i].add(self.position)))
        return edges
    
    
    
    def getXYPoints(self):
        points = []
        for i in range(0, len(self.corners)):
            p = self.corners[i].add(self.position)
            points.append(p.xy())
        return points
    
    def Points(self):
        return self.getXYPoints()
        
    def draw(self, screen):
        points = self.getXYPoints()
        for i in range(-1,len(points)-1):
            pygame.draw.line(screen,(250,0,0,100), points[i],points[i+1] ) 
    '''

def getPolygonFromPoints(pts):
    vectors = []
    if len(pts) == 0:
        return vectors
    (x, y) = pts[0]
    vectors.append(Vector2.Vector2(0, 0))
    for i in range (1, len(pts)):
        vectors.append(Vector2.Vector2(pts[i][0] - x, pts[i][1] - y))
    return ((x, y), vectors)


    
