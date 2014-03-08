'''
Created on Jan 28, 2014

@author: otrebor
'''
'''
points are not world points is a set of vectors using x,y as reference point, to simplify movement
'''
import pygame
import Shape
import game.util.Vector2 as Vector2


class Polygon(Shape.Shape):
    yaml_tag =u'!Polygon'
    def __getstate__(self):
        data = Shape.Shape.__getstate__(self)
        data['corners'] = self.corners
        return data
        
    def __init__(self,transform, (x,y) = (0,0), points = []):
        Shape.Shape.__init__(self, transform)
        self._offset = (x,y)
        self._corners = [ Vector2.Vector2(pt.x, pt.y) for pt in points ]
        self._cache = self._corners
        self._angle = -999
        self.calAABB()
        
    def calAABB(self):
        corners = self.corners
        self.aabb = (min([pt.x for pt in corners]),
                     min([pt.y for pt in corners]),
                     max([pt.x for pt in corners]),
                     max([pt.y for pt in corners]))
        
    @property
    def corners(self):
        if self._angle != self.transform.angle:
            self._angle = self.transform.angle
            self._cache = []
            for point in self._corners:
                self._cache.append(point.rotate(self._angle))
        return self._cache
        
    @property
    def offset(self):
        return self._offset
    
    @offset.setter
    def offset(self,value):
        self._offset = value
        
    @property
    def center(self):
        return self.transform.position.add(Vector2.Vector2(*self.offset))
    
    @property
    def left(self):
        return self.aabb[0] + self.position.x
    
    @property
    def top(self):
        return self.aabb[1] + self.position.y
    
    @property
    def right(self):
        return self.aabb[2] + self.position.x
    
    @property
    def bottom(self):
        return self.aabb[3] + self.position.y
    
    @property
    def width(self):
        return self.right - self.left
    
    @property
    def height(self):
        return self.bottom - self.top
    
    @property
    def startCorner(self):
        return (self.left, self.top)
    
    @property    
    def endCorner(self):
        return (self.right, self.bottom)
    
    def draw(self, screen):
        points = self.getXYPoints()
        for i in range(-1,len(points)-1):
            pygame.draw.line(screen,(250,0,0,100), points[i],points[i+1] ) 
    
    def getPoints(self):
        corners = self.corners
        points = []
        for i in range(0, len(corners)):
            points.append(corners[i].add(self.position))
        return points
    
    def getEdges(self):
        corners = self.corners
        edges = []
        for i in range(0, len(corners)):
            edges.append((corners[i - 1].add(self.position), corners[i].add(self.position)))
        return edges
    
    def getXYPoints(self):
        corners = self.corners
        points = []
        for i in range(0, len(corners)):
            p = corners[i].add(self.position)
            points.append(p.xy())
        return points
    
    
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
    
    def getPoints(self):
        points = []
        for i in range(0, len(self.corners)):
            points.append(self.corners[i].add(self.position))
        return points
    
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


    
