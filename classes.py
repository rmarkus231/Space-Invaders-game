#import sys
import pygame as pg
import numpy as np
import cv2

class Bullet(pg.sprite.Sprite):
    speed = 4
    def __init__(self,pos):
        super().__init__()
        self.image = pg.Surface((pos[0],pos[1]))
        self.image = pg.image.load("./graphics/bullet_s.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.rect.scale_by_ip(0.4)
        
        #print(type(self.rect))
        #self.rect = pg.rect.Rect(1,1,1,1,center = pos)
    
    def update(self,collides = False):
        self.rect.y -= self.speed
        if self.rect.y < 0 or collides:
            self.kill()

class Game():
    #save window w/h to class local arg
    width = 0
    height = 0
    def __init__(self,w,h):
        self.width = w
        self.height = h
        p_sprite = Player((self.width/2 ,self.height))
        self.player = pg.sprite.GroupSingle(p_sprite)
        self.def_group = Defense(self.width,(10,self.height-50),10,100)
    
    
    def run(self,screen):
        self.def_group.shape_group.draw(screen)
        #self.Defense_group.sprite.shape_group.update() #no update func yet
        self.collides()
        self.player.sprite.bullet_group.update()
        self.player.sprite.bullet_group.draw(screen)
        self.player.draw(screen)
        self.player.update()
    
    def collides(self):
        for b in self.player.sprite.bullet_group:
            col = pg.sprite.spritecollide(b,self.def_group.shape_group,True)
            if col:
                b.kill()
                #col.kill()
        

class Player(pg.sprite.Sprite):
    #How many pixels it moves / frame
    speed = 3
    pos = None
    ready = True
    time = 0
    cooldown = 300
    bullet_group = None
    def __init__(self,pos):
        super().__init__()
        self.pos = (pos[0]*2,float(pos[1]))
        self.image = pg.image.load("./graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        
        self.bullet_group = pg.sprite.Group()
    
    def move(self):
        k = pg.key.get_pressed()
        if k[pg.K_RIGHT] and (self.rect.x + self.speed < self.pos[0]-32): # minus sprite width
            self.rect.x += self.speed
        if k[pg.K_LEFT] and (self.rect.x - self.speed > 0):
            self.rect.x -= self.speed
        if k[pg.K_SPACE] and self.ready:
            self.ready = False
            self.time = pg.time.get_ticks()
            self.shoot()

    def charge(self):
        if not self.ready:
            time = pg.time.get_ticks()
            if time -self.time > self.cooldown:
                self.ready = True
    
    def shoot(self):
        #create bullet at player current middle position
        self.bullet_group.add(Bullet(self.rect.center))
    
    def update(self):
        self.move()
        self.charge()
"""
class Target(pg.sprite.Sprite):
    x = 300
    y = 300
    def __init__(self,x,y,colour):
        super().__init__()
        
        self.image = pg.image.load("/graphics/red.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        
        if color == 'red': self.value = 100
        elif color == 'yellow': self.value = 200
        else: self.value = 300
		
    def update(self,direction):
        self.rect.x += direction
"""

class Pixel(pg.sprite.Sprite):
    x = 0
    y = 0
    def __init__(self,x,y,color):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pg.Surface((1,1))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

class Defense(pg.sprite.Sprite):
    shape = []
    shape_group = None
    def __init__(self,width,pos,gaps,offset):
        super().__init__()
        self.img_2_shape()
        self.shape_group = pg.sprite.Group()
        """
        Uses numpy array as basis to make a group of pixels
        """
        #equal distribution of defensive 
        positions = np.linspace(
            0+offset/2,
            width-offset,
            num = gaps
            )
        #print(positions)
        
        for row_i,val1 in enumerate(self.shape):
            for col_i,val2 in enumerate(val1):
                if sum(val2) != 0:
                    #Since cv2 uses bgr and image is in rgp, swap b & r
                    val2[0], val2[2] = val2[2], val2[0]
                    clr = tuple(val2)
                    #print(clr)
                    for i,p in enumerate(positions):
                        #print(p)
                        self.shape_group.add(Pixel(
                            pos[0]+col_i+ p,
                            pos[1]+row_i,
                            clr))
                            #self.shape_group.add(Pixel(pos[0]+col_i,pos[1]+row_i,clr))
        #print(self.shape_group)
    
    def img_2_shape(self):
        #converts image to numpy array
        self.shape = cv2.imread('graphics/barrier.png')
        