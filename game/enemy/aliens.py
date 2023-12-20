import pygame as pg
import numpy as np
import math as m

class Aliens(pg.sprite.Sprite):
    aliens = None
    def __init__(self,width,height,rows,cols,x_gap_size,y_gap_size,alien_speed = 0):
        super().__init__()
        self.width = width
        self.height = height
        self.alien_speed = alien_speed
        self.alien_direction = 1
        self.aliens = pg.sprite.Group()
        self.dif = 3
        #colors = ["purple","red","yellow"]
        
        #image dims
        self.dim = 32
        positions = np.linspace(
                y_gap_size,
                width-y_gap_size-self.dim,
                num = cols
            )
        
        for _,pos in enumerate(positions):
            for row_i in range(rows):
                x = pos
                y = 50+row_i*(self.dim+x_gap_size)
                
                if row_i <= 1:
                    clr = "yellow"
                elif 1 < row_i <= 3:
                    clr = "purple"
                else:
                    clr = "red"
                
                self.aliens.add(Alien(clr,x,y))
        self.alien_total = len(self.aliens)
    
    def update(self):
        self.current_aliens = (len(self.aliens))
        self.alien_speed = self.alien_direction*(1-round(((self.current_aliens/self.alien_total)-1)*self.dif,4))
        #print("alien speed:",self.alien_speed)
        self.aliens.update(self.alien_speed)
    
    def alien_down(self):
        self.alien_direction *= -1
        for a in self.aliens:
            a.rect.y += abs(self.alien_speed*3)
        self.update()
    
    def set_difficulty(self,new):
        self.dif = new
    
    def getAmount(self):
        return (len(self.aliens))
                
class Alien(pg.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.color = color
        file = "./graphics/"+color+".png"
        self.image = pg.image.load(file).convert_alpha()
        self.rect = self.image.get_rect( topleft = (x,y))
    
    def update(self,speed, **kwargs):
        if "Down" in kwargs and kwargs["Down"] == True:
            self.rect.y += abs(speed)
        else:
            self.rect.x += speed

class SpecialAlien(pg.sprite.Sprite):
    def __init__(self,w,h):
        super().__init__()
        self.width = w
        self.height = h
        self.speed = 8
        
        #0 = hide
        #1 = up right
        #2 = up left
        #3 = fly
        #4 = go down
        self.state = 0
        
        file = "./graphics/ufo.png"
        self.image = pg.image.load(file).convert_alpha()
        self.rect = self.image.get_rect( topleft = (8,-43)) #spawns out of screen space
        self.retreat = [8,self.width-8]
        
        self.worthList = [100, 50, 50, 100, 150, 100, 100, 50, 300, 100, 100, 100, 50, 150, 100, 50]
        self.worth = 0
    
    
    def update(self):
        if self.state == 3:
            print("flying")
            self.rect.x += abs(self.speed)
            self.Hide()
        elif self.state in [1,2]:
            print("leaving")
            self.goUp()
        elif self.state == 0:
            print("hiding")
            self.standStill()
        elif self.state == 4:
            print("coming down")
            self.goDown()
        
    def increment(self):
        self.worth += 1
        if self.worth > (len(self.worthList)-1):
            self.worth = 0
    
    def inBounds(self):
        if self.rect.x > 0 and self.rect.y > 0:
            return True
        else:
            return False
    
    def standStill(self):
        pass
    
    def goDown(self):
        self.rect.y += 1
        if self.rect.y == 8:
            self.state = 3
    
    def goUp(self):
        self.rect.y -= 1
        if self.rect.y == -43:
            self.state = 0
    
    def changeDirection(self):
        self.speed *= -1
    
    def Hide(self):
        if (self.ttl - pg.time.get_ticks()) < 0:
            if self.rect.x == self.retreat[0]:
                self.state = 1
            elif self.rect.x == self.retreat[0]:
                self.state = 2

    def activate(self):
        self.state = 4
    
    def setTTL(self,arg): #time to live, in ms
        self.ttl = pg.time.get_ticks() + arg