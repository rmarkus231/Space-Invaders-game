#import sys
import pygame as pg
import numpy as np
import cv2
#from pygame.sprite import _Group
import math as m
import random

class Bullet(pg.sprite.Sprite):
    def __init__(self,pos,lim ,direction = True,speed = 4, img = "./graphics/bullet_s.png", clr = "white"):
        super().__init__()
        self.speed = speed
        self.clr = clr
        self.image = pg.Surface((pos[0],pos[1]))
        self.image = pg.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.threshold = lim
        self.direction = direction
        self.rect.scale_by_ip(0.4)
        
        #print(type(self.rect))
        #self.rect = pg.rect.Rect(1,1,1,1,center = pos)
    
    def update(self,collides = False):
        self.rect.y -= self.speed
        if self.direction:
            if self.rect.y < self.threshold or collides:
                self.kill()
        else:
            if self.rect.y > self.threshold or collides:
                self.kill()

class Game():
    #save window w/h to class local arg
    width = 0
    height = 0
    ready = False
    alien_cooldown = 1000 #in ms
    def __init__(self,w,h):
        self.width = w
        self.height = h
        p_sprite = Player((self.width/2 ,self.height))
        self.player = pg.sprite.GroupSingle(p_sprite)
        self.def_group = Defense(self.width,(10,self.height-50),10,100)
        self.aliens = Aliens(self.width,self.height,7,10,5,50,alien_speed= 1)
        #had to put the alien bullet group here because it would
        #NOT FUCKING DRAW if it was in the aliens class, POS
        self.alien_lasers = pg.sprite.Group()
        self.time = pg.time.get_ticks()
    
    
    def run(self,screen):
        self.alien_lasers.update()
        self.player.sprite.bullet_group.update()
        self.aliens.update()
        self.player.update()
        
        self.collides()
        self.charge()
        if self.ready:
            self.alien_shoot()
            self.ready = False
            self.time = pg.time.get_ticks()
        
        self.def_group.shape_group.draw(screen)
        self.player.sprite.bullet_group.draw(screen)
        self.player.draw(screen)
        self.aliens.aliens.draw(screen)
        self.alien_lasers.draw(screen)
    
    def collides(self):
        for b in self.player.sprite.bullet_group:
            col = pg.sprite.spritecollide(b,self.def_group.shape_group,True)
            if col:
                b.kill()
                #col.kill()
        for ab in self.alien_lasers:
            col = pg.sprite.spritecollide(ab,self.def_group.shape_group,True)
            if col:
                if ab.clr != "yellow":
                    ab.kill()
    
    def alien_shoot(self):
        if self.aliens.aliens:
            a = random.choice(self.aliens.aliens.sprites())
            file = "./graphics/a_bullet_"+a.color+".png"
            self.alien_lasers.add(Bullet(a.rect.center,self.height,False,speed=-4, img = file,clr = a.color))
    
    def charge(self):
        if not self.ready:
            time = pg.time.get_ticks()
            if time -self.time > self.alien_cooldown:
                self.ready = True

                
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
        self.bullet_group.add(Bullet(self.rect.center,0))
    
    def update(self):
        self.move()
        self.charge()

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
    
    def img_2_shape(self):
        #converts image to numpy array
        self.shape = cv2.imread('graphics/barrier.png')

class Aliens(pg.sprite.Sprite):
    aliens = None
    def __init__(self,width,height,rows,cols,x_gap_size,y_gap_size,alien_speed = 0):
        super().__init__()
        self.width = width
        self.height = height
        self.alien_speed = alien_speed
        self.aliens = pg.sprite.Group()
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
    
    def update(self):
        self.alien_checker()
            
    
    def alien_checker(self):
        for a in self.aliens:
            if a.rect.x <= 0 or a.rect.x+self.dim >= self.width:
                self.alien_speed *= -1
                if self.aliens:
                    self.alien_down()
        self.aliens.update(self.alien_speed)
    
    def alien_down(self):
        for a in self.aliens:
            a.rect.y += abs(self.alien_speed)
                
class Alien(pg.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.color = color
        file = "./graphics/"+color+".png"
        self.image = pg.image.load(file).convert_alpha()
        self.rect = self.image.get_rect( topleft = (x,y))
    
    def update(self,speed):
        self.rect.x += speed