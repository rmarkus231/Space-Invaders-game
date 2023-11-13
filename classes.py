import sys
import pygame as pg

class Bullet(pg.sprite.Sprite):
    speed = 10
    def __init__(self,pos):
        super().__init__()
        self.image = pg.Surface((pos[0],pos[1]))
        self.image = pg.image.load("./graphics/bullet.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
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
    
    
    def run(self,screen):
        self.player.sprite.bullet_group.update()
        self.player.sprite.bullet_group.draw(screen)
        self.player.draw(screen)
        self.player.update()

class Player(pg.sprite.Sprite):
    #How many pixels it moves / frame
    speed = 5
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
    def __init__(self,x,y):
        x = 0
        y = 0
        super().__init__()
        self.image = pg.image.load("./graphics/alien.png").convert_alpha()
        self.rect = self.image.get_rect(topleft =(x,y))
"""