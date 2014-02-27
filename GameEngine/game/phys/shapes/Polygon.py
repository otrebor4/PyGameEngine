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
        
    def __init__(self, x, y, points):
        # points are vectors from the reference point (x,y)
        Shape.Shape.__init__(self, x, y)
        self.corners = [ Vector2.Vector2(pt.x, pt.y) for pt in points ]
        self.aabb = (min([pt.x for pt in self.corners]),
                     min([pt.y for pt in self.corners]),
                     max([pt.x for pt in self.corners]),
                     max([pt.y for pt in self.corners]))
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
            pygame.draw.line(screen,(250,0,0,100), points[i],points[i+1] ) #(screen, (250,0,100), self.getXYPoints())
            
        #s = pygame.Surface([self.Width(), self.Height()], pygame.SRCALPHA, 32)
        #s.fill((250, 0, 0, 100))
        
        
        #screen.blit(scr, (self.Left(), self.Top()))
        pass

def getPoligonFromPoints(pts):
    vectors = []
    if len(pts) == 0:
        return vectors
    (x, y) = pts[0]
    vectors.append(Vector2.Vector2(0, 0))
    for i in range (1, len(pts)):
        vectors.append(Vector2.Vector2(pts[i][0] - x, pts[i][1] - y))
    return ((x, y), vectors)


    
