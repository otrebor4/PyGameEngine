'''
Created on Feb 13, 2014

@author: Otrebor45
'''
import pygame
import Vector2
import game.util.LineTest as LineTest
import game.lib.yaml as yaml

class Node:
    def __init__(self,value = None):
        self.next = None
        self.value = value
    def eq(self,val):
        return self.value == val
    
class Graph(yaml.YAMLObject):
    yaml_tag = '!Graph'
    
    
    def __init__(self, points = None):
        self.Debug = False
        self.edges = {}
        if points:
            for i in range(-1, len(points)-1):
                self.edges[ points[i]] = [ points[i+1]]
        self.first = None
           
    def connect(self, v1, v2):
        self.edges[v1] = self.edges[v1] if v1 in self.edges.keys() else []
        if not v2 in self.edges[v1]:
            self.edges[v1].append(v2)
              
    def addEdge(self,v1,v2,strict = False):
        self.edges[v1] = self.edges[v1] if v1 in self.edges.keys() else []
        if strict:
            self.edges[v1] = [v2]
        else:
            self.edges[v1].append(v2)
        
        if v1 in  (self.edges[v2] if v2 in self.edges.keys() else []):
            self.edges[v2].remove(v1)
            if v2 in self.edges[v1]:
                self.edges[v1].remove(v2)
            if not len(self.edges[v1]):
                self.edges.pop(v1)
            if v2 in self.edges and not len(self.edges[v2]):
                self.edges.pop(v2)
    
    def Segment(self, v1, v2, segments):
        segment = []
        for (c1,c2) in segments:
            if (c1[0] < v1[0] or c1[1] < v1[1])  and (c2[0] > v2[0] or c2[1] > v2[1]):
                i = segment.index( (c1,c2))
                segment.pop( (c1,c2))
                segment.insert(i, (c1,v1))
                segment.insert(i+1, (c2,v2))
                break
            else:
                segment.append((c1,c2))
        return segment
    
    def AddEdge(self, v1,v2):
        segments = [(v1,v2)]
        
        _in = self.MakeVector(v1, v2).normalize()
        edges =self.getIntersectionEdges((v1,v2))
        for e in edges:
            out = self.MakeVector(e[0], e[1])
            if _in.calAngle(out) == 180:
                segments = self.Segment(v1, v2, segments)
        
        for (c1,c2) in segments:
            self.addEdge(c1, c2)
        
    def intersects(self, edge):    
        for e in self.getEdges():
            if (edge[0] == e[1]) or (edge[1] == e[0]) or (edge[0] == e[0]) or ( edge[1] == e[1]):
                #if self.isPointOnLine(edge, e[0]) and self.isPointOnLine(edge, e[1]) or self.isPointOnLine(e, edge[0]) and self.isPointOnLine(e, edge[1]):
                #    return True
                continue
            if self.intersect(e, edge):
                if self.Debug:
                    self.drawLine(e[0], e[1], (200,200,200))
                    self.drawLine(edge[0], edge[1], (0,200,200))
                    pygame.time.wait(500)
                
                return True
        return False
    
    def getIntersectionEdges(self, edge):
        edges = []
        for e in self.getEdges():
            if self.intersect(e, edge):
                edges.append(e)
        return edges
    
    '''
        LineB2 = edge2[1]
        LineB1 = edge2[0]
    
        LineA2 = edge1[1]
        LineA1 = edge1[0]
        denom = ((LineB2[1] - LineB1[1]) * (LineA2[0] - LineA1[0])) - ((LineB2[0] - LineB1[0]) * (LineA2[1] - LineA1[1]))
       
        return denom != 0
    '''
   
    def getFirstVertex(self):
        current = None
        for k in self.edges.keys():
            if current:
                if k[0] < current[0] and k[1] < current[1]:
                    current = k
            else:
                current = k
        return current
        
    def getFirst(self):
        for k in self.edges.keys():
            return (k,self.edges[k])
        return (None,None)
    
    def getPolygon(self,v):
        circle = []
        circle.append(v)
        #circle.first = v
        if not self.edges.has_key(v):
            return None
        _next = self.edges[v]
        if not len(_next):
            return None
        _next = _next[0]
        close = False
        while _next and not close:
            if _next in circle:
                close = True
                continue
            circle.append(_next)
            _next = self.edges[_next]
            if not len(_next):
                return None
            _next = _next[0]
        return circle
            
    def cross(self, graph):
        for edge in graph.edges:
            v1 = edge
            en = graph.edges[edge]
            if len(en):
                v2 = en[0]
                self.addEdge(v2, v1)

    def getBest(self, _in, v1, v2):
        best = v2[0]
        b = 360
        for v in v2:
            out = self.MakeVector(v1, v).normalize()
            ang = _in.calAngle(out)
            if ang < b:
                b = ang
                best = v
        return best
    
    def getCicles(self):
        if self.Debug:
            self.cls()
            self.print_graph( (0,255,0))
        circles = []
        
        _r = 0
        _g = 0
        _b = 50
        v1 = None
        while len(self.edges):
            circle = Graph()
            if not v1 or not self.edges.has_key(v1):
                v1 = self.getFirstVertex()
            #if v1 is self.edges.has_key(v1):
            v2 = self.edges[v1]
            if len(v2) <= 0:
                continue
            v2 = v2[0]
            circle.addEdge(v1, v2)
            circle.first = v1
            finish = False
            while not finish:
                v3 = v1
                v1 = v2
                if not self.edges.has_key(v2):
                    finish = True
                    continue
                _in = self.MakeVector(v1, v3).normalize()
                v2 = self.edges[v2]
                if len(v2) <= 0:
                    continue
                if len(v2) > 1:
                    v2 = self.getBest(_in, v1, v2)
                else:
                    v2 = v2[0]
                out = self.MakeVector(v1, v2).normalize()
                if not self.TestAngle(_in, out):# or self.intersects( (v1,v2)):
                    done = False
                    v2 = v1
                    while not done:
                        parents = self.getParents(v2)
                        v2 = self.getBest(_in, v2, parents)
                        out = self.MakeVector(v1, v2)
                        ang = _in.calAngle(out)
                        if (ang == 90 or ang == 180) and not self.intersects( (v1,v2)):
                            parents = self.getParents(v2)
                            v3 = v2
                            v3 = self.getBest(_in, v3, parents)
                            _out = self.MakeVector(v1, v3)
                            _nang = _in.calAngle(_out)
                            while _nang == ang == 180:
                                v2 = v3
                                parents = self.getParents(v3)
                                v3 = self.getBest(_in, v3, parents)
                                _out = self.MakeVector(v1, v3)
                                _nang = _in.calAngle(_out)
                                self.drawLine( v2, v3)
                                
                            if v2 in circle.edges.keys():
                                finish = True
                            done = True
                elif v1 in circle.edges.keys():
                    finish = True
                
                circle.addEdge(v1,v2,True)
                if self.Debug:
                    
                    self.print_graph((0,255,0))
                    circle.print_graph()
                    
                    pygame.time.wait(200)
            
            poly = circle.getPolygon(v2)
            g = Graph( poly)
            self.cross(g)
            if self.Debug:
                self.cls()
                self.print_graph( (0,255,0))
            circles.append(poly)
        return circles  
    
    def getEdges(self):
        edges = []
        for k in self.edges.keys():
            for v in self.edges[k]:
                edges.append( (k,v))
        return edges
    
    def getParents(self,v):
        keys = []
        for key in self.edges:
            if v in self.edges[key]:
                keys.append(key)
        return keys
    
    def TestAngle(self, v1, v2 ,_range=[0,180]):
        ang = v1.calAngle(v2) 
        return (ang > _range[0] and ang <= _range[1])
    
    def MakeVector(self,v1,v2):
        return Vector2.Vector2(v2[0],-v2[1]).sub( Vector2.Vector2(v1[0],-v1[1]))
    
    
    def drawLine(self, v1, v2, color = (0,255,0),screen=None):
        flip = False
        if not screen:
            screen = pygame.display.get_surface()
            flip = True
        pygame.draw.line( screen,color, v1, v2 )
        if flip:
            pygame.display.flip()
    
    def print_graph(self, color = (255,0,0,100),screen=None):
        flip = False
        if not screen:
            screen = pygame.display.get_surface()
            flip = True
        for key in self.edges:
            for end in self.edges[key]:
                pygame.draw.line( screen,color, key, end )
                if flip: 
                    pygame.display.flip()
        
    def drawPolygon(self, points, color = (250,250,250,10)):
        screen = pygame.display.get_surface()
        pygame.draw.polygon(screen, color, points  )
        #pygame.display.flip()
        
    def cls(self):
        screen = pygame.display.get_surface()
        screen.fill( (0,0,0))
        
        
    '''
    def intersect(self,line1, line2):
        
        self.drawLine(line1[0], line1[1], (200,0,0))
        self.drawLine(line2[0], line2[1], (0,0,200))
        pygame.time.wait(100)
        p1 = line1[0] 
        q1 = line1[1]
        p2 = line2[0]
        q2 = line2[1]
        o1 = self.orientation(p1, q1, p2);
        o2 = self.orientation(p1, q1, q2);
        o3 = self.orientation(p2, q2, p1);
        o4 = self.orientation(p2, q2, q1);
 
        if (o1 != o2 and o3 != o4):
            return True;
        
        if (o1 == 0 and self.onSegment(p1, p2, q1)):
            return True
     
        if (o2 == 0 and self.onSegment(p1, q2, q1)):
            return True
 
        if (o3 == 0 and self.onSegment(p2, p1, q2)):
            return True
        if (o4 == 0 and self.onSegment(p2, q1, q2)):
            return True
 
        return False
        '''
    def orientation(self, p,  q,  r):
        val = (q[1] - p[1]) * (r[1] - q[1]) -(q[1] - p[1]) * (r[1] - q[1]);
        if (val == 0):
            return 0
        return 1 if val > 0 else 2

    
    def onSegment(self, p, q, r):
        if (q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]) and q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
            return True
        return False;


    def lineSegmentTouchesOrCrossesLine(self, seg1, seg2):
            return self.isPointOnLine(seg1, seg2[0])  or self.isPointOnLine(seg1, seg2[1]) or self.isPointRightOfLien(seg1, seg2[0]) and self.isPointRightOfLien(seg1, seg2[1]) 
        
    
    
    def isPointOnLine(self, linea, p):
        aTmp = Vector2.Vector2( linea[0][0] - linea[1][0], linea[0][1]-linea[1][1] )
        pTmp = Vector2.Vector2( p[0] - linea[1][0], p[1]-linea[1][1] )
        r = aTmp.x * pTmp.y - pTmp.x * aTmp.y;
        return abs(r) < 0.000001
    
    def isPointRightOfLien(self, linea, p):
        aTmp = Vector2.Vector2( linea[0][0] - linea[1][0], linea[0][1]-linea[1][1] )
        pTmp = Vector2.Vector2( p[0] - linea[1][0], p[1]-linea[1][1] )
 
        return aTmp.cross(pTmp) < 0
    
    def intersect(self,line1, line2):
        if self.Debug:
            self.drawLine(line1[0],line1[1], (200,0,0))
            self.drawLine(line2[0], line2[1], (0,0,200))
        return LineTest.calculateIntersectPoint(line1[0], line1[1], line2[0], line2[1])
        #return self.lineSegmentTouchesOrCrossesLine(line1, line2) and self.lineSegmentTouchesOrCrossesLine(line2, line1)
        
        
        
        
        
