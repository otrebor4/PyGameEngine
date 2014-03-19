'''
Created on Jan 28, 2014

@author: otrebor
'''
'''
Rectangle position is the left top corner
'''

import Polygon
import gameEngine.util.Vector2 as Vector2

class Rectangle(Polygon.Polygon):
    def __init__(self, transform, (x,y)=(0,0),(w,h) = (0,0), angle=0):
        self.offset = (x,y)
        points = [Vector2.Vector2(-w/2, -h/2),
                  Vector2.Vector2(w/2, -h/2),
                  Vector2.Vector2(w/2, h/2),
                  Vector2.Vector2(-w/2, h/2)]
        Polygon.Polygon.__init__(self, transform, (x, y), points, angle = 0)
