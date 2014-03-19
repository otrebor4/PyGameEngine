'''
Created on Jan 29, 2014

@author: otrebor
'''
import pygame
debug = False

lines = []

def Log(msg):
    if debug:
        print msg

def LogError(msg):
    if debug:
        print "Error: %(s)" % (msg)

def drawLine( p1, p2, color = (0,0,0) ):
    global lines
    lines.append( (p1,p2,color))


def draw(screen):
    global lines
    if not debug:
        lines = []
        return
    for p1,p2,color in lines:
        pygame.draw.line(screen,color,p1,p2)
    lines = []