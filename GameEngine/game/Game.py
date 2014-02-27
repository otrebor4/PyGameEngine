'''
Created on Jan 30, 2014

@author: otrebor
'''
import sys

import pygame
import game.Debug as Debug
import pygame.locals as locals
import util.Vector2 as Vector2
import world
import Resources
import random

def init():
    random.seed(pygame.time.get_ticks())

def getNextRange( min, max ):
    return random.randrange( min, max )

class Game:
    DEBUG = False
    RESOLUTION = (1024, 768)
    GAMENAME = "null"
    INIT = False        
    _instance = None
    @classmethod
    def Instance(cls):    
        return cls._instance
    
    @classmethod
    def setInstance(cls,inst):    
        cls._instance = inst
    
    def ToggleFullScreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.RESOLUTION, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.RESOLUTION)
        
    def __init__ (self):
        self.fullscreen = True
        self.ToggleFullScreen()
        Game.setInstance(self)
        self.INIT = True
        pygame.init()
        self.resources = Resources.Resources() 
        
        pygame.display.set_caption(self.GAMENAME)
        #pygame.display.toggle_fullscreen()
        
        if not hasattr(self, 'world'):
            self.world = world.World(self, self.RESOLUTION, Vector2.Vector2(0, 0))
            
        self.fps = 0
        self.fps_time = 0
        self.delta = 0
        #self.skipGUI = True
        
    def draw(self):
        self.fps_time += self.delta
        if self.fps_time > 1:
            self.fps_time -= 1
            self.fps = 0
        
        self.screen.fill((0, 0, 0, 0))
        self.world.draw(self.screen)
        self.world.OnGUI(self.screen)
        if self.DEBUG:
            self.world.debDraw(self.screen)
        Debug.draw(self.screen)
        pygame.display.flip()
        self.fps += 1
        return
        
    def update(self, delta):
        pygame.event.pump()
        for evt in pygame.event.get():
            if evt.type == locals.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.key.get_pressed()[locals.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        if pygame.key.get_pressed()[locals.K_F4]:
            self.ToggleFullScreen()
        self.world.update(delta)
        
        return
    
    def run(self):
        if not self.INIT:
            self.init()
        oldtime = pygame.time.get_ticks()
        pygame.time.wait(5)
        while True:
            newtime = pygame.time.get_ticks()
            delta = newtime - oldtime
            oldtime = newtime
            deltaf = delta / 1000.0
            self.delta = deltaf
            self.update(deltaf)
            self.draw()
    def Delta(self):
        return self.delta
            
    def Load(self,data):
        pass
    def Reset(self):
        pass
