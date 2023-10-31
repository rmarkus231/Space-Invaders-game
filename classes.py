import sys
import pygame as pg

class bullet():
    x = 0
    y = 0
    w = 0
    h = 0
    time = None
    dead = False
    
    def __init__(self,x1,y1,w1,h1,time = None):
        self.x = x1
        self.y = y1
        self.w = w1
        self.h = h1
        self.time = time
    
    def update_params(self,x1,y1,w1,h1,):
        self.x = x1
        self.y = y1
        self.w = w1
        self.h = h1
    
    def draw(self,screen):
        self.image = pg.draw.rect(screen, (0,255,0), (self.x,self.y,self.w,self.h))
    
    def update(self,tk,kt = 250):
        if self.time is not None:
            #if kill_time ms have passed, kill instance of object
            self.kill_time = kt    #200ms
            if tk - self.time >= self.kill_time:
                #self.kill()
                self.dead = True
        