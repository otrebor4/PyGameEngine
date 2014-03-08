'''
Created on Jan 28, 2014

@author: otrebor
'''
'''
Rectangle position is the left top corner
'''

import Polygon
import game.util.Vector2 as Vector2

class Rectangle(Polygon.Polygon):
    yaml_tag = u'!Rectangle'
    def __init__(self, transform, (x,y)=(0,0), (w,h)=(0,0)):
        self.offset = (x,y)
        points = [Vector2.Vector2(-w/2, -h/2),
                  Vector2.Vector2( w/2, -h/2),
                  Vector2.Vector2( w/2,  h/2),
                  Vector2.Vector2(-w/2,  h/2)]
        self._width = w
        self._height= h
        Polygon.Polygon.__init__(self, transform, (x,y), points)
