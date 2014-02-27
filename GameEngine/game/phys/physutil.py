'''
Created on Jan 22, 2014

@author: otrebor
'''
import math

import game.phys.shapes.Circle
import game.phys.shapes.Polygon
import game.util.Vector2 as Vector2


class CollisionInfo:
    def __init__(self):
        self.shape1 = None
        self.shape2 = None
        self.distance = 0
        self.direction = Vector2.Vector2()  # normal vector
        

# fast aabb overlap check

def checkAABBOverlap(obj1, obj2):
    aabb1 = obj1.gameObject.shape.calAABB() if obj1.gameObject.shape != None else None
    aabb2 = obj2.gameObject.shape.calAABB() if obj2.gameObject.shape != None else None
    
    if aabb1 == None or aabb2 == None:  # missing at least one shape can't collide
        return False
    
    return not (aabb1[3] < aabb2[1] or
                 aabb1[1] > aabb2[3] or
                 aabb1[0] > aabb2[2] or
                 aabb1[2] < aabb2[0])



# return a collisionInfo if happen or None if not collision detected

def testCollision(obj1, obj2):
    if not checkAABBOverlap(obj1, obj2):
        return None
    shape1 = obj1.gameObject.shape
    shape2 = obj2.gameObject.shape
    # circle circle collision
    if isinstance(shape1, game.phys.shapes.Circle.Circle) and isinstance(shape2, game.phys.shapes.Circle.Circle):
        return testCircleCircle(shape1, shape2)
        
    # polygon polygon collision
    if isinstance(shape1, game.phys.shapes.Polygon.Polygon) and isinstance(shape2, game.phys.shapes.Polygon.Polygon):
        return testPolygonSat(shape1, shape2)
        
    # polygon-circle collision
    if isinstance(shape1, game.phys.shapes.Circle.Circle):
        return testCirclePolygonSat(shape1, shape2, False)
    else:
        return testCirclePolygonSat(shape2, shape1, True)
           
def testCircleCircle(c1, c2):
    totalRadius = c1.radius + c2.radius
    distSqr = c1.position.distanceSq(c2.position)
    if distSqr > totalRadius * totalRadius:
        return None
    else:
        info = CollisionInfo()
        info.shape1 = c1
        info.shape2 = c2
        info.direction = c1.position.sub(c2.position).normalize()
        
        info.distance = math.sqrt(distSqr) - totalRadius;
        return info
        
def testPolygonSat(poly1, poly2):
    shortestDist = INF
    
    result = CollisionInfo()
    result.shape1 = poly1
    result.shape2 = poly2
    
    p1 = poly1.getPoints()
    p2 = poly2.getPoints()
    # get offset
    # vOffset = Vector2.Vector2()# poly1.position.sub(poly2.position)
    
    for i in range(0, len(p1)):
        vAxis = getAxisNormal(p1, i)
        # project polygon 1
        (min0, max0) = getMinMax(vAxis, p1)
                
        # project polygon 2
        (min1, max1) = getMinMax(vAxis, p2)
        
        # sOffset = vAxis.dot(vOffset)
        # min0 = min0 + sOffset
        # max0 = max0 + sOffset
        
        (dist, new) = makeResult(result, min0, max0, min1, max1, vAxis, True)
        if dist <= shortestDist:
            shortestDist = dist
            if new == None:
                return None
            result = new
        
    return result
    
def testCirclePolygonSat(circle, polygon, flip):
    dist = INF
    shorterDist = INF
    closestPoint = Vector2.Vector2()
    result = CollisionInfo()
    if flip:
        result.shape1 = polygon
        result.shape2 = circle
    else:
        result.shape1 = circle
        result.shape2 = polygon
        
    p1 = polygon.getPoints()
    
    # get offset
    # vOffset = Vector2.Vector2()#circle.position.sub(polygon.position)
    # find closes point
    for p in p1:
        currentDist = p.distance(circle.position)
        if currentDist < dist:
            dist = currentDist
            closestPoint.x = p.x
            closestPoint.y = p.y
    
    vAxis = closestPoint.sub(circle.position).normalize()
    # project polygon
    (min0, max0) = getMinMax(vAxis, p1)
    
    # project circle
    min1 = vAxis.dot(circle.position)
    max1 = min1 + circle.radius
    min1 = min1 - circle.radius
    
    # sOffset = vAxis.dot(p1[0])
    # min0 = min0 + sOffset
    # max0 = max0 + sOffset
    
    (dist, new) = makeResult(result, min0, max0, min1, max1, vAxis, flip)
    if dist < shorterDist:
        shorterDist = dist
        if new == None:
            return None
        result = new
    
    for i in range(0, len(p1)):
        vAxis = getAxisNormal(p1, i)
        (min0, max0) = getMinMax(vAxis, p1)
                
        # project circle
        min1 = vAxis.dot(circle.position)
        max1 = min1 + circle.radius
        min1 = min1 - circle.radius
    
        # sOffset = vAxis.dot( vOffset)
        # min0 = min0 + sOffset
        # max0 = max0 + sOffset
    
        (dist, new) = makeResult(result, min0, max0, min1, max1, vAxis, flip)
        if dist < shorterDist:
            shorterDist = dist
            if new == None:
                return None
            result = new
        
    return result

def makeResult(old, min0, max0, min1, max1, vAxis, flip=False):
    result = CollisionInfo()
    result.shape1 = old.shape1
    result.shape2 = old.shape2
    if max0 < min1:
        return (0, None)
    if max1 < min0:
        return (0, None)
    distmin = (max1 - min0) if flip else -(max1 - min0)
    distminAbs = -distmin if distmin < 0 else distmin
    result.distance = distminAbs
    if distmin < 0:
        result.direction = vAxis.scale(-1).normalize()
    else:
        result.direction = vAxis.normalize()
    
    return (distminAbs, result)
    
def getMinMax(axis, p1):
    min0 = axis.dot(p1[0])
    max0 = min0
        
    for j in range(1, len(p1)):
        t = axis.dot(p1[j])
        if t < min0:
            min0 = t
        if t > max0:
            max0 = t
    return (min0, max0)

def getAxisNormal(points, index):
    pt1 = points[index]
    pt2 = points[ index + 1 if index + 1 < len(points) else 0 ]
    return pt2.sub(pt1).normal().normalize()
    
    
    
# obj1 and obj2 are GameObjects, edge is a (Vector2, Vector2)

def HandleCollision(obj1, obj2, info):
    # only riged component respond to collision
    rig1 = obj1.gameObject.riged   
    rig2 = obj2.gameObject.riged
    if (rig1 == None or rig1.kinematic) and (rig2 == None or rig2.kinematic):  # why try to handle collision they don't respond to collision
        return 
    normal = info.direction.normalize()
    
    v1 = rig1.velocity if rig1 != None else Vector2.Vector2()
    ns1 = normal.dot(v1)
    v1x = normal.scale(ns1)
    v1y = v1.sub(v1x)
        
    normal.scale(-1)
    
    v2 = rig2.velocity if rig2 != None else Vector2.Vector2()
    ns2 = normal.dot(v2)
    v2x = normal.scale(ns2)
    v2y = v2.sub(v2x)
    
    if (rig2 == None):
        rig1.velocity = v1x.scale(-1).add(v1y)
    elif (rig1 == None):
        rig2.velocity = v2x.scale(-1).add(v2y)
    else:   
        m1 = rig1.mass if rig1 != None else INF
        m2 = rig2.mass if rig2 != None else INF
        cm = m1 + m2
        if not rig1.kinematic:
            rig1.velocity = v1x.scale((m1 - m2) / cm).add(v2x.scale((2 * m2) / cm)).add(v2y)
        if not rig2.kinematic:
            rig2.velocity = v1x.scale((2 * m1) / cm).add(v2x.scale((m2 - m1) / cm)).add(v2y)
    
INF = 1000000000
def div(x, y):
    # x/y
    if y == 0:
        return INF
    if y > INF:
        return 0
    return x / y


def PolygonInsidePolygon( poly1, poly2 ):
    #check if poly1 is inside poly2
    inside = True
    for (x,y) in poly1:
        inside = inside and pointInsidePolygon((x,y), poly2)
        
    return inside

def pointInsidePolygon( (x,y), poly):
    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

