'''
Created on Feb 17, 2014

@author: otrebor
'''
from collections import deque
import bisect
import graph
import Vector2


class NavMesh(graph.Graph):
    yaml_tag = u'!NavMesh'
    def __init__(self, points=None):
        graph.Graph.__init__(self, points=points)
        self.Debug = False
        self.data = None
        
    def addEdge(self,v1,v2, strict = False, mesh = False):
        if mesh:
            self.edges[v1] = self.edges[v1] if v1 in self.edges.keys() else []
            if not v2 in self.edges[v1]:
                self.edges[v1].append(v2)
        else:
            graph.Graph.addEdge(self, v1, v2, strict)
        
    def remove(self, v):
        if self.edges.has_key(v):
            self.edges.pop(v)
        for k in self.edges.keys():
            if v in self.edges[k]:
                self.edges[k].remove(v)
                if not len(self.edges[k]):
                    self.edges.pop(v)
    
    def findNext(self,v):
        if self.edges.has_key(v):
            return self.edges[v][0]
        return None
    
    def simplifyGraph(self):
        g = NavMesh()
        end = None
        if len(self.edges):
            v0 = self.getCorner()
            v1 = self.findNext(v0)
            if v1:
                v2 = self.findNext(v1)
            else:
                v2 = v0
            end = v0
            while v2 != end:
                _in = self.MakeVector(v0, v1).normalize()
                _out = self.MakeVector(v0, v2).normalize()
                if self.Debug:
                    self.drawLine(v0, v1,(0,255,0))
                    self.drawLine(v1, v2,(0,0,255))
                    graph.pygame.time.wait(100)
                ang = _in.calAngle(_out)
                if ang == 0:
                    v1 = v2
                    v2 = self.findNext(v2)
                    
                else:
                    g.addEdge(v0,v1)
                    v0 = v1
                    v1 = v2
                    v2 = self.findNext(v2)
                if v2 == end:
                    g.addEdge(v0,v1)
                    g.addEdge(v1,v2)
                if self.Debug:
                    g.print_graph(None)
                    graph.pygame.time.wait(100)
        return g
    
    
        '''
        g = NavMesh()
        if len(self.edges):
            v0 = self.edges.keys()[0]
            v1 = self.edges[v0][0]
            visited = []
            while not v0 in visited:
                self.print_graph()
                
                _in = self.MakeVector(v1, v0).normalize()
                self.drawLine(v1, v0, (0,255,0))
                v2 = self.edges[v1]
                if len(v2) <= 0:
                    continue
                visited.append(v0)
                if len(v2) > 1:
                    v2 = self.getBest(_in, v1, v2)
                    v0 = v1
                    v1 = v2
                    g.addEdge(v0,v1)
                    continue
                else:
                    v2 = v2[0]
                    out = self.MakeVector(v1, v2).normalize()
                    self.drawLine(v1, v2, (0,0,255))
                    ang = _in.calAngle(out)
                    if ang == 180:
                        g.remove(v1)
                        g.addEdge(v0, v2)
                        v1 = v2
                        visited.remove(v0)
                    else:
                        v0 = v1
                        v1 = v2
                        v2 = None
                graph.pygame.time.wait(100)
    '''
    
    def getNext(self,v1):
        for v2 in self.edges[v1]:
            if not v1 in self.edges[v2]:
                return v2  
        return None
    
    def makeTrig(self):
        if not len(self.edges.keys()):
            return
        v0 = self.edges.keys()[0]
        v1 = self.getNext(v0)
        while v1 != None:
            v2 = self.getNext(v1)
            self.addEdge(v1,v0,False,True)
            self.addEdge(v2,v1,False,True)
            self.addEdge(v0,v2,False,True)
            v1 = self.getNext(v0)
        
    def addPoly(self,poly):
        for (v1,v2) in poly.getEdges():
            self.addEdge(v1, v2, False,True)
    
    def getLowerCorners(self, _set):
        current = None
        amount = -1
        for nav in _set:
            corners = nav.getCorners()
            count = len(corners)
            if not current:
                current = nav
                amount = len(corners)
            elif count < amount:
                current = nav
                amount = count
        return current
                
    def getCornersRange(self,p, r):
        v1 = Vector2.Vector2(p[0],p[1])
        points = []
        for p2 in self.getCorners():
            v2 = Vector2.Vector2(p2[0],p2[1])
            if v2.distance(v1) <= r:
                points.append(p2)
        return points
        
    def getCorner(self):
        for k in self.edges.keys():
            v1 = self.findNext(k)
            v2 = self.findNext(v1)
            _in = self.MakeVector(k, v1).normalize()
            out = self.MakeVector(v1, v2).normalize()
            ang = _in.calAngle(out)
            if ang != 0:
                return v1
       
    def getCorners(self):
        corners = []
        for k in self.edges.keys():
            v1 = self.findNext(k)
            v2 = self.findNext(v1)
            _in = self.MakeVector(k, v1).normalize()
            out = self.MakeVector(v1, v2).normalize()
            ang = _in.calAngle(out)
            if ang != 0:
                corners.append(k)
        return corners
             
    def getPolygons(self):
        if self.Debug:
            #print "makingPolygons"
            
            self.cls()
            self.print_graph( (0,255,0))
            graph.pygame.time.wait(500)
        circles = []
        
        _r = 0
        _g = 0
        _b = 50
        v1 = None
        while len(self.edges):
            circle = NavMesh()
            if not self.edges.has_key(v1):
                v1 = self.getFirstVertex()
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
                    visited = []
                    while not done and not( v2 in visited):
                        visited.append(v2)
                        parents = self.getParents(v2)
                        v2 = self.getBest(_in, v2, parents)
                        out = self.MakeVector(v1, v2).normalize()
                        ang = _in.calAngle(out)
                        if (ang > 0 and ang <= 180) and not self.intersects( (v1,v2)):
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
                                #self.drawLine( v2, v3)
                                
                            if v2 in circle.edges.keys():
                                finish = True
                            done = True
                elif v1 in circle.edges.keys():
                    finish = True
                
                circle.addEdge(v1,v2,True)
                if self.Debug:
                    self.print_graph((0,255,0))
                    circle.print_graph(None)
                    graph.pygame.time.wait(500)
            
            poly = circle.getPolygon(v2)
            g = NavMesh( poly)
            self.cross(g)
            if self.Debug:
                self.cls()
                self.print_graph( (0,255,0))
            circles.append(poly)
        return circles 
    
    def separateGraph(self):
        navs = []
        
        while len(self.edges):
            nav = NavMesh()
            v0 = self.getCorner()
            v1 = self.findNext(v0)
            start = v0
            while v1 != start:
                self.addEdge(v1, v0)
                nav.addEdge(v0, v1)
                v0 = v1
                v1 = self.findNext(v1)
                if v1 == start:
                    self.addEdge(v1, v0)
                    nav.addEdge(v0, v1)
                
                if self.Debug:
                    nav.print_graph(None,(0,255,0))
                    graph.pygame.time.wait(100)
            
            navs.append(nav)
            
        for i in range(0, len(navs)):
            navs[i] = navs[i].simplifyGraph()
            self.addPoly(navs[i])
            
        while len(navs) > 1:
            nav = self.getLowerCorners(navs)
            navs.remove(nav)
            corners = nav.getCorners()
            for p in corners:
                for p1 in self.getCornersRange(p,200):
                    if not p1 in corners and not self.intersects((p,p1)):
                        self.connect(p1, p)
                        self.connect(p, p1 )
                        break
                    
    def makeNavMesh(self):
        #self.Debug = True
        self.separateGraph()
        self.data = NavMeshData(self)
        
        '''
        self.data.draw_graph(None, (100,0,0))
        p1=Vector2.Vector2(200,200)
        p2=Vector2.Vector2(600,300)
        self.drawLine(p1.xy(), p2.xy(), (0,255,0))
        graph.pygame.time.wait(1000)
        path = self.GetPath(p1,p2)
        path.draw(graph.pygame.display.get_surface(), (0,0,255))
        graph.pygame.display.flip()
        graph.pygame.time.wait(5000)
        '''
        
        return self
        #self.simplifyGraph()
        #self.makeTrig()
        #g = self.simplifyGraph()
        #self.print_graph()
        #circles = self.getPolygons()
        #self.makeTrig()    
        #circles = self.getPolygons()
        #for poly in circles:
        #    poly = NavMesh(poly)
        #    poly.simplifyGraph()
        #    poly.makeTrig()
        #    self.addPoly(poly)
        #self.simplifyGraph()
        #self.makeTrig()
        #self.print_graph()
        #graph.pygame.time.wait(10000)
    

    def print_graph(self, screen=None, color=(255, 0, 0, 100)):
        #if not screen:
        #    screen = graph.pygame.display.get_surface()
        if self.data:
            self.data.draw_graph(screen,color)

    
    def GetPath(self, start, goal):
        return Path(start, goal, self.data)
        
    
    
###############################  
#  
#   
###############################   
    
    
    
def winding_sign( a, b ):
    c = b.x * a.y - a.x * b.y 
    return -1 if c < 0 else (1 if c > 0 else 0 )
    
    
# holds a particular navmesh node (w/ best cost) during pathfinding
#  edge_in is a tuple ((x,y),(x,y))
class PathStep:
    def __init__( self, cost, node, edge_in, target ):
        self.node = node
        self.cost = cost
        # straight distance heuristic
        self.est_cost = node.distance( target )
        # pointer to prior step, used in path search
        self.prior = None
        # cache edge in (may change during pathfinding)
        self.edge_in = edge_in
        self.target = target

    def __eq__( self, other ):
        if isinstance( other, PathStep ):
            return self.node == other.node
        return NotImplemented

    def __ne__( self, other ):
        if isinstance( other, PathStep ):
            return not self.__eq__( other )
        return NotImplemented

    def __lt__( self, other ):
        if isinstance( other, PathStep ):
            # sort by reverse cost (to allow popping)
            return self.total_cost() > other.total_cost()
        return NotImplemented

    def __str__( self ):
        return "PathStep: %s via %s, cost: %f" % (self.node,self.edge_in,self.cost)

    # calculate distance from the edge into me to the proposed edge out
    def edge_edge_distance( self, edge_out ):
        if self.edge_in:
            start = Vector2.mid( *self.edge_in )
        else:
            start = self.node.centroid
        return Vector2.mid( *edge_out ).sub( start ).magnitude()

    # for the funnel algorith, return left endpoint of edge_in from the
    #  perspective of pt
    def left_endpoint_in( self, pt ):
        e0 = Vector2.Vector2(*self.edge_in[0])
        e1 = Vector2.Vector2(*self.edge_in[1])
        ws = winding_sign( e0.sub( pt ), e1.sub( pt ) )
        #assert ws != 0, "Left endpoint call on colinear line %s, %s" % (pt,self.edge_in)
        if ws == -1:
            # goes left to right
            return e0
        else:
            return e1

    def right_endpoint_in( self, pt ):
        e0 = Vector2.Vector2(*self.edge_in[0])
        e1 = Vector2.Vector2(*self.edge_in[1])
        ws = winding_sign( e0.sub( pt ), e1.sub( pt ) )
        #assert ws != 0, "Right endpoint call on colinear line %s, %s" % (pt,self.edge_in)
        if ws == 1:
            # goes right to left
            return e0
        else:
            return e1

    def total_cost( self ):
        # centroid based
        #return self.cost + self.est_cost
        # edge based
        if self.edge_in is None:
            return self.cost + self.est_cost
        else:
            return self.cost + self.target.centroid.sub( Vector2.mid( *self.edge_in ) ).magnitude()

    # cost to neighbor Node (not PathStep!)
    # edge_in is transition edge from self to neighbor
    def cost_to( self, neighbor, edge_in ):
        return self.cost + Vector2.mid( *edge_in ).sub( self.node.centroid ).magnitude()
        

# path identifies navmesh nodes to traverse and waypoints
#  on the edges of those nodes
# the best (most direct) nodes and waypoints are identified first
#  to be used as reference for learned behavior
# repathing can probably be made more efficient by keeping
#  intermediate structures
class Path:
    def __init__( self, start, end, nm, start_node=None,stoplist=[] ):
        self.start = start
        self.end = end
        self.nm = nm
        self.current = None
        if start_node is None:
            self.start_node = nm.get_node_from_point( start )
        else:
            self.start_node = start_node


        self.path_steps = []
        self.init_path_steps(  stoplist )

        self.funnel_points = []
        self.calc_funnel_points()

        self.index = 0
        self.findex = 0

    def len( self ):
        return len( self.funnel_points ) + 1

    # assumes first segment in funnel path!
    def intersection( self, edge_sig ):
        e0,e1 = Vector2.edge_from_sig( edge_sig )

        ip = None
        if len(self.funnel_points) > 0:
            ip = Vector2.segment_intersect( self.start, self.funnel_points[0], e0, e1 )
        elif len( self.path_steps ) > 0:            
            ip = Vector2.segment_intersect( self.start, self.end, e0, e1 )
        return ip

    # returns the edge (e0,e1) containing pt and the path index of the node
    #  that edge leads into (can be last node in path)
    def funnel_point_edge( self, pt ):
        i = 0
        for ps in self.path_steps:
            if pt.xy() == ps.edge_in[0] or pt.xy() == ps.edge_in[1]:
                return (Vector2.Vector2( *ps.edge_in[0] ),Vector2.Vector2( *ps.edge_in[1] )),i
            i += 1
        return None,None
    
    def __eq__( self, other ):
        if isinstance( other, Path ):
            return self.path_steps == other.path_steps
        return NotImplemented

    def __ne__( self, other ):
        if isinstance( other, Path ):
            return not self.__eq__( other )
        return NotImplemented

    def __str__( self ):
        if len(self.path_steps) == 0:
            return "Path: Empty"
        return "Path: %s" % ' '.join( [str(ps.node) for ps in self.path_steps] )            

    def first_node( self ):
        if len(self.path_steps) > 0:
            return self.path_steps[0].node
        return None

    def first_unclimbable( self ):
        for ps in self.path_steps:
            if not ps.node.enterable_from( ps.edge_in ):
                return ps.node
        return None
    
    def init_path_steps( self,  stoplist ):
        end_node = self.nm.get_node_from_point( self.end )
        if not end_node or not self.start_node:
            return
        if self.start_node == end_node:
            return
        
        frontier = [PathStep( 0, self.start_node, None, end_node )]
        done = {}
        
        # best-first based on distance to goal
        while len( frontier ) > 0:
            best = frontier.pop()
            for edge_in,neighbor in best.node.neighbors.items():
                if neighbor == end_node:
                    self.path_steps.append( PathStep( best.cost_to( neighbor, edge_in  ), neighbor, edge_in, end_node ) )
                    while best.prior:
                        self.path_steps.append( best )
                        best = best.prior
                    self.path_steps.reverse()
                    return
                if neighbor in stoplist:
                    continue
                

                # see if this is new or improved from prior paths
                ncost = best.cost_to( neighbor, edge_in  )
                #print "ncost to %s is %f" % (neighbor,ncost)
                if neighbor in done:
                    pn = done[neighbor]
                    if ncost < pn.cost:
                        # this is a better path to get here
                        pn.cost = ncost
                        pn.prior = best
                        pn.edge_in = edge_in
                        # remove and re-add to frontier
                        pos = bisect.bisect_right( frontier, pn )
                        if pos == 0 or frontier[pos-1] != pn:
                            # not in frontier, put it there
                            frontier.insert( pos, pn )
                        else:
                            # is in frontier, remove and readd for sorting
                            del frontier[pos-1]
                            bisect.insort( frontier, pn )
                else:
                    # never been here
                    pn = PathStep( ncost, neighbor, edge_in, end_node )
                    pn.prior = best
                    done[neighbor] = pn
                    bisect.insort( frontier, pn )
                    
    def init(self):
        self.reset()
        self.current = self.start
        
    # like path steps, doesn't include start or end
    
    def calc_funnel_points( self ):
        self.funnel_points = []
        
        # trivial case
        if len(self.path_steps) < 1:
            return

        # funnel algorithm
        apex = self.start
        vl = self.path_steps[0].left_endpoint_in( apex )
        vr = self.path_steps[0].right_endpoint_in( apex )
        f = deque( [vl,apex,vr] )
        for i in range(1,len(self.path_steps)):
            ## check for straight line if apex has changed
            #if newapex != apex:
            #    print "checking direct path from %s to %s" % (newapex,self.end)
            #    if self.contains_line( newapex, self.end ):
            #        # straight path works from newapex
            #        print "...found!"
            #        if newapex != self.start:
            #            self.funnel_points.append( newapex )
            #        return
            #    print "...no"
            #    apex = newapex

            # set mid for next l/r distinction
            mid = vl.add( vr.sub( vl ).scale( 0.5 ) )

            ps = self.path_steps[i]
            
            
            #print "checking edge %s" % (ps.edge_in,)

            # left first
            vl_next = ps.left_endpoint_in( mid )
            if vl_next != vl:
                vl = vl_next
                #print "adding left %s" % vl
                apex = self.funnel_add_left( f, apex, vl )
                
                #print "...apex %s" % apex

            # then right
            vr_next = ps.right_endpoint_in( mid )
            if vr_next != vr:
                vr = vr_next
                #print "adding right %s" % vr
                apex = self.funnel_add_right( f, apex, vr )
                
                #print "...apex %s" % apex

        # add end point to either side to finish the path
        #print "adding goal %s" % self.end
        apex = self.funnel_add_left( f, apex, self.end )
        # add add that side of the funnel (minus goal) to the path
        f.popleft()
        ending = []
        v = f.popleft()
        while v != apex:
            ending.append( v )
            v = f.popleft()
        ending.append( apex )
        ending.reverse()
        self.funnel_points.extend( ending )

        # get rid of start point
        self.funnel_points = self.funnel_points[1:]

    # start is assumed to be on a corner in the path_steps
    # and end is assumed to be beyond the final edge
    
    def contains_line( self, start, end ):
        for i in range(len(self.path_steps)-1,0,-1):
            ps = self.path_steps[i]
            # see if this is the edge that start is on
            if start.xy() in ps.edge_in:
                # made it, must be true
                return True
            #print "...contains check on %s" % (ps.edge_in,)
            if Vector2.segment_intersect( start, end,\
                                       Vector2.Vector2(*ps.edge_in[0]),\
                                       Vector2.Vector2(*ps.edge_in[1]) ) is None:
                return False
        # never found start, false
        return False

    def funnel_add_left( self, f, apex, v ):
        while True:
            #print "...l/a/r: %s/%s/%s" % (f[0],apex,f[-1])

            # 0 is left, -1 is right in deque
            if f[0] == f[-1]: # left == right (not apex?)
                #print "...left == right"
                f.appendleft( v )
                break

            # check which way left->v winds
            if f[0] == apex: # left == apex
                vlast = f[1].sub( f[0] )
                vnew = v.sub( f[0] )
            else:
                vlast = f[0].sub( f[1] )
                vnew = v.sub( f[0] )

            # if winds the same way (counterclockwise for left)
            if vlast.rotation_to( vnew ) < 0:
                # just append and done
                #print "...same winding direction, adding %s to funnel" % v
                f.appendleft( v )
                break

            #print "...different winding, popping"

            # if we're on the apex and it didn't wind the same way,
            #  move the apex and continue
            if f[0] == apex: # left == apex
                #print "...moving apex"
                self.funnel_points.append( f.popleft() ) # pop apex and add to path
                apex = f[0] # new leftmost is new apex
            else:
                f.popleft()

        return apex

    def funnel_add_right( self, f, apex, v ):
        while True:
            #print "...l/a/r: %s/%s/%s" % (f[0],apex,f[-1])

            # 0 is left, -1 is right in deque
            if f[0] == f[-1]: # left == right (not apex?)
                #print "...left == right"
                f.append( v )
                break

            # check which way left->v winds
            if f[-1] == apex: # right == apex
                vlast = f[-2].sub( f[-1] )
                vnew = v.sub( f[-1] )
            else:
                vlast = f[-1].sub( f[-2] )
                vnew = v.sub( f[-1] )

            # if winds the same way (clockwise for right)
            if vlast.rotation_to( vnew ) > 0:
                # just append and done
                #print "...same winding direction, adding %s to funnel" % v
                f.append( v )
                break

            #print "...different winding, popping"

            # if we're on the apex and it didn't wind the same way,
            #  move the apex and continue
            if f[-1] == apex: # right == apex
                #print "...moving apex"
                self.funnel_points.append( f.pop() ) # pop apex and add to path
                apex = f[-1] # new rightmost is new apex
            else:
                f.pop()

        return apex

    def reset( self ):
        self.index = 0
        self.findex = 0
        self.current = None
    # mid to return midpoints
    # displacement off of funnel point in midpoint direction
    # specify train to return funnel point, mid point and edge (e0,e1)
    
    def getWayPoint(self):
        return self.current
        '''
        if self.index == -1 or self.index > len(self.funnel_points):
            return None
        if len(self.path_steps) == 0:
            return None
        if self.index == len(self.funnel_points):
            return self.end
        
        return self.funnel_points[self.index]
        '''
    
    def getNextWaypoint(self, r = 0):
        self.current = self.nextWaypoint(r)
        #self.current = self.next_waypoint( mid = False, displacement = r)
        return self.current
        '''
        if self.index == -1:
            return None
        if len(self.path_steps) == 0:
            return None
        if self.index > len(self.funnel_points):
            self.index  = -1;
            return None
        if self.index == len(self.funnel_points):
            self.index += 1
            return self.end
        self.index += 1
        return self.funnel_points[self.index-1]
        '''
    
    
    def nextWaypoint(self, radius=0.0):
        if self.findex == -1:
            return None
        if self.findex == len(self.funnel_points):
            self.findex = -1
            return self.end
        if radius == 0:
            self.findex += 1
            return self.funnel_points[self.findex-1]
        
        prev = self.funnel_points[self.findex-1] if self.findex > 0 else self.start
        curr = self.funnel_points[self.findex]
        nxt = self.funnel_points[self.findex+1] if self.findex+1 < len(self.funnel_points) else self.end
        
        
        vp = curr.sub(prev).normalize()
        vn = curr.sub(nxt).normalize()
        
        offset = vp.add(vn)
        offset = offset.normalize().scale(radius)
        
        curr = curr.add(offset)
        self.findex += 1
        return curr
        
        
    
    def next_waypoint( self, mid=False, displacement=0.0, train=False ):
        if self.index == -1:
            # no more path
            if train:
                return None,None,None
            else:
                return None

        if self.index == len( self.path_steps ):
            # last one, return end point
            self.index = -1
            if train:
                return self.end,self.end,None
            return self.end

        # get next edge
        p1,p2 = self.path_steps[self.index].edge_in
        self.index += 1
        e1 = Vector2.Vector2( *p1 )
        e2 = Vector2.Vector2( *p2 )

        if mid:
            # return midpoint path, for visualization
            return e1.add( e2.sub( e1 ).scale( 0.5 ) )

        # set fp to funnel point on next edge
        if self.findex == len(self.funnel_points):
            nextf = self.end
        else:
            nextf = self.funnel_points[self.findex]
            
        if nextf.xy() == e1.xy() or nextf.xy() == e2.xy():
            # at the funnel point edge, return and advance
            fp = nextf
            self.findex += 1
        else:
            # otherwise get the intersection with the edge
            if self.findex > 0:
                lastf = self.funnel_points[self.findex-1]
            else:
                lastf = self.start
            fp = Vector2.intersection( lastf, nextf, e1, e2 )

        # need midpoint for direction of displacement
        mp = e1.add( e2.sub( e1 ).scale( 0.5 ) )

        if train:
            return fp,mp,(e1,e2)

        if displacement == 0:
            return fp

        disp = mp.sub( fp ).normalize().scale( displacement )
        return fp.add( disp )
        
    # length of all segments combined
    
    def length( self ):
        pts = [self.start]
        pts.extend( self.funnel_points )
        pts.append( self.end )
        return sum( Vector2.map_pairs( pts, fn=lambda v1,v2: v2.sub(v1).magnitude() ) )
    
    def getWayPoints(self):
        points = [self.start]
        index = self.index
        findex = self.findex
        self.index = 0
        self.findex = 0
        current = self.nextWaypoint(25)#next_waypoint(False, 10)
        while current:
            points.append(current)
            current = self.nextWaypoint(25)#next_waypoint(False, 10)
        self.index = index
        self.findex = findex
        return points
    
    def draw(self,screen,color = (0,0,255)):
        points = self.getWayPoints()
        for i in range(0, len(points)-1):
            p1 = points[i]
            p2 = points[i+1]
            graph.pygame.draw.line(screen, color, p1.xy(),p2.xy() )
            #graph.pygame.display.flip()
            #graph.pygame.time.wait(100)
        
class PolyNode(graph.yaml.YAMLObject):
    yaml_tag = u'!PolyNode'
    def __init__( self, points):
        self.corners = [Vector2.Vector2( *pt ) for pt in points]
        # dude, counter-clockwise!
        self.corners.reverse()
        self.neighbors = {}
        self.aabbox = (min([pt.x for pt in self.corners]),
                       min([pt.y for pt in self.corners]),
                       max([pt.x for pt in self.corners]),
                       max([pt.y for pt in self.corners]))
        # cache centroid and sample heights at edges, center
        self.calc_centroid()
        
    
    def __str__( self ):
        return "<PolyNode: %s>" % ', '.join( str(c) for c in self.corners )

    # eq/hash only good when drawing from the same pool of points, otherwise
    #  floating point imprecision, etc.
    def __eq__( self, other ):
        if isinstance( other, PolyNode ):
            return self.corners == other.corners
        return NotImplemented

    def __ne__( self, other ):
        if isinstance( other, PolyNode ):
            return not self.__eq__( other )
        return NotImplemented
    
    def __hash__( self ):
        return hash( tuple(self.corners) )

    def other_point( self, points ):
        for c in self.corners:
            if c not in points:
                return c

    # check if you can enter from this edge due to height change
    def enterable_from( self, edge_in ):
        # true if not sloped, not unclimable, or not going up from the
        #  specified edge_in
        return 's' not in self.feats or \
               'u' not in self.feats or \
               self.centroid_h <= self.edge_hs[edge_in]

    def edge_sigs( self ):
        for i in range(0,len(self.corners)-1):
            yield self.edge_sig(self.corners[i],self.corners[i+1])
        yield self.edge_sig(self.corners[-1],self.corners[0])

    def edge_sig( self, c1, c2 ):
        if c1 < c2:
            return (c1.xy(),c2.xy())
        return (c2.xy(),c1.xy())

    def add_neighbor( self, other, edge, reflexive=True ):
        if not self.neighbors.has_key( edge ):
            self.neighbors[edge] = other
            other.add_neighbor( self, edge, False )
        else:
            # has this key, better be the same poly
            assert self.neighbors[edge] == other, "Overlapping edges found in mesh"

    def calc_area( self ):
        a = b = 0
        for i in range(-1,len(self.corners)-1):
            a += self.corners[i].x * self.corners[i+1].y
            b += self.corners[i].y * self.corners[i+1].x
        self.area = 0.5 * (a - b)
        return self.area

    def calc_centroid( self ):
        cx = cy = 0.0
        for i in range(-1,len(self.corners)-1):
            det = self.corners[i].x * self.corners[i+1].y - self.corners[i+1].x * self.corners[i].y
            cx += (self.corners[i].x + self.corners[i+1].x) * det
            cy += (self.corners[i].y + self.corners[i+1].y) * det
        area = self.calc_area()
        self.centroid = Vector2.Vector2( cx / 6 / area, cy / 6 / area )
        return self.centroid
    
    def distance( self, p ):
        if not p:
            return -1
        return p.centroid.sub( self.centroid ).magnitude()

    def bbox_contains( self, v ):
        return v.x >= self.aabbox[0] and v.x <= self.aabbox[2] and v.y >= self.aabbox[1] and v.y <= self.aabbox[3]
            
    def contains( self, v ):
        if not self.bbox_contains( v ):
            return False
        # use winding method
        tc = self.translated_corners( v )
        sign = winding_sign( tc[-1], tc[0] )
        if sign == 0:
            # v is on this edge
            return True
        for i in range(0,len(tc)-1):
            nxt = winding_sign( tc[i], tc[i+1] )
            if nxt == 0:
                return True
            if nxt != sign:
                return False
        return True

    # return a new translated corner set by vector v
    
    def translated_corners( self, v ):
        return [c.sub( v ) for c in self.corners]
    
    
class NavMeshData(graph.yaml.YAMLObject):
    yaml_tag = u'!NavMeshData'
    def __init__( self, nm ):
        self.polys = []
        self.build_mesh( nm )
        self.nm = nm

    def build_mesh( self, nm ):

        edge_index = {}
        for pol in nm.getPolygons():
            p = PolyNode(pol)
            for e in p.edge_sigs():
                # establish any connections
                if edge_index.has_key( e ):
                    for otherp in edge_index[e]:
                        p.add_neighbor( otherp, e )
                        # and add self to edge index
                    edge_index[e].append( p )
                else:
                    # just add self to edge index
                    edge_index[e] = [p]

            # and add to mesh
            self.polys.append( p )
            
        '''
        for feats,pts in REGIONS_A:
            # make next poly
            p = PolyNode( pts, feats )
            
            # for each edge
            for e in p.edge_sigs():
                
                # establish any connections
                if edge_index.has_key( e ):
                    for otherp in edge_index[e]:
                        p.add_neighbor( otherp, e )
                        # and add self to edge index
                    edge_index[e].append( p )
                else:
                    # just add self to edge index
                    edge_index[e] = [p]

            # and add to mesh
            self.polys.append( p )
        '''
    
    def get_node_from_point( self, v ):
        for p in self.polys:
            if p.contains( v ):
                return p
        return None
    
    def toPairs(self,pts):
        pairs =[ ]
        for v in pts:
            pairs.append(v.xy())
        return pairs
    
    
    def draw_graph(self,screen=None,color=(255,0,0)):
        
        for poly in self.polys:
            points = poly.corners
            #screen = graph.pygame.display.get_surface()
            for i in range(-1,len(points)-1):
                graph.Graph.drawLine(self.nm, (points[i].xy()), (points[i+1].xy()),  color,screen)
            #    graph.pygame.display.flip()
            #    graph.pygame.time.wait(1000)
            #graph.pygame.draw.polygon(screen,(0,250,0,100), self.toPairs(points) )
            #graph.pygame.display.flip()
            #graph.pygame.time.wait(1000)
        
        