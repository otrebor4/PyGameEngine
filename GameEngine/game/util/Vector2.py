'''
Created on Jan 22, 2014

@author: otrebor
'''
import math

E=0.001

def mid( a, b ):
    if not isinstance( a, Vector2 ):
        a = Vector2( *a )
        b = Vector2( *b )
    return a.add( b.sub( a ).scale( 0.5 ) )

def edge_from_sig( sig ):
    return (Vector2( *sig[0] ),Vector2( *sig[1] ))

def intersect_v( corner, h, start, end ):
    if abs(start.x - end.x) < E:
        return None
    if abs(start.y - end.y) < E:
        return Vector2( corner.x, start.y )

    d = end.sub( start )
    islope = d.y / float(d.x)

    intersectx = corner.x
    intersecty = start.y + islope * (intersectx - start.x)

    return Vector2( intersectx, intersecty )

def intersection( start1, end1, start2, end2 ):
    if abs(start1.x - end1.x) < E:
        return intersect_v( start1, (end1.y-start1.y), start2, end2 )
    elif abs(start2.x - end2.x) < E:
        return intersect_v( start2, (end2.y-start2.y), start1, end1 )
     
    d1 = end1.sub( start1 )
    slope1 = d1.y / float(d1.x)

    d2 = end2.sub( start2 )
    slope2 = d2.y / float(d2.x)

    if abs(slope1 - slope2) < E:
        return None

    intersectx = (start1.y - slope1 * start1.x - start2.y + slope2 * start2.x) / (slope2 - slope1)
    intersecty = start1.y + slope1 * (intersectx - start1.x)

    return Vector2( intersectx, intersecty )


def segment_intersect( start1, end1, start2, end2 ):
    sxr1 = segment_xrange( start1, end1 )
    sxr2 = segment_xrange( start2, end2 )
    if not ranges_overlap( sxr1, sxr2 ):
        return None

    syr1 = segment_yrange( start1, end1 )
    syr2 = segment_yrange( start2, end2 )
    if not ranges_overlap( syr1, syr2 ):
        return None

    ip = intersection( start1, end1, start2, end2 )
    if ip is not None and within( ip.x, sxr1 ) and within( ip.x, sxr2 ):
        return ip
    return None

def segment_xrange( start, end ):
    return( min(start.x,end.x), max(start.x,end.x) )

def segment_yrange( start, end ):
    return( min(start.y,end.y), max(start.y,end.y) )

def ranges_overlap( r1, r2 ):
    if r1[1] < r2[0] or r2[1] < r1[0]:
        return False
    return True

def within( x, r ):
    return x >= r[0]-E and x <= r[1]+E

def map_pairs( l, key=None, test=None, fn=None ):
    #print "map pairs: %s" % ', '.join( [str(e) for e in l] )
    if len(l) < 2:
        return []
    result = []
    prior = use_key( l[0], key )
    for i in range(1,len(l)):
        nxt = use_key( l[i], key )
        if test is not None and not test( prior, nxt ):
            prior = nxt
            continue
        if fn is not None:
            result.append( fn( prior, nxt ) )
        else:
            result.append( (prior,nxt) )
        prior = nxt
    return result

def use_key( val, fn ):
    if fn is None:
        return val
    return fn( val )

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "(%0.2f, %0.2f)" % (self.x, self.y)
    
    def __repr__(self):
        return self.__str__()
    
    def add(self, v2):
        return Vector2(self.x + v2.x, self.y + v2.y)
    
    def sub(self, v2):
        return Vector2(self.x - v2.x, self.y - v2.y)
    
    def scale(self, s):
        return Vector2(self.x * s, self.y * s)
    
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self):
        m = self.magnitude()
        if m == 0:
            return Vector2()
        return Vector2(self.x / m, self.y / m)
    
    def normal(self):
        return Vector2(self.y, -self.x)
    
    def distance(self, v2):
        return math.sqrt(math.pow((self.x - v2.x), 2) + math.pow((self.y - v2.y), 2))
    
    # distance square used on circle collision
    def distanceSq(self, v2):
        return math.pow((self.x - v2.x), 2) + math.pow((self.y - v2.y), 2)
    
    def dot(self, v2):
        return self.x * v2.x + self.y * v2.y
    
    def cross(self, v2):
        return Vector2(self.x * v2.y, self.y * v2.x)
    
    def multiply(self,v2):
        return Vector2(self.x * v2.x, self.y * v2.y)
    
    def xy(self):
        return (self.x, self.y)
    
    def angle(self):
        angle = math.atan2(self.y, self.x)*(180/math.pi)
        if angle < 0:
            angle += 360
        return angle
    def calAngle(self,v2):
        a1 = v2.angle()
        a2 = self.angle()
        angle =  a1-a2
        return angle if angle >= 0 else angle + 360
        #return self.sub(v2).angle()
    def rotate(self,angle):
        ang = angle+self.angle()
        ang = ang *(math.pi/180)
        x = math.cos(ang)*self.magnitude()
        y = math.sin(ang)*self.magnitude()
        return Vector2(x,y)
    
    def rotation_to( self, other ):
        theta = math.atan2( self.y, self.x )
        theta_other = math.atan2( other.y, other.x )

        theta_diff = theta_other - theta

        # handle wrap-around
        if theta_diff > math.pi:
            theta_diff -= 2 * math.pi
        elif theta_diff < -1 * math.pi:
            theta_diff += 2 * math.pi

        return theta_diff

    # eq/ne/hash only useful for comparing same points from a data set,
    #  otherwise floating point inaccuracy etc.
    def __eq__( self, other ):
        if isinstance( other, Vector2 ):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __hash__( self ):
        return hash( self.xy() )

    def __ne__( self, other ):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    # sort x than y
    def __lt__( self, other ):
        return self.x < other.x or (self.x == other.x and self.y < other.y)
    
Zero  = Vector2(0,0)
Up    = Vector2(0,1)
Down  = Vector2(0,-1)
Left  = Vector2(-1,0)
Right = Vector2(1,0)

'''
Testing purposes...
if __name__ == '__main__':
    v1 = Vector2(1,0)
    v2 = Vector2(1,-1)
    a1 = v1.angle()
    a2 = v2.angle()
    print v1
    print v2
    print v1.calAngle(v2)
    print v1.rotate(90).angle()
    print v1.rotate(45).angle()
    print v1.rotate(180).angle()
    print v1.rotate(281).angle()
'''