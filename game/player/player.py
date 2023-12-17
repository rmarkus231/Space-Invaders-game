import pygame as pg
from ..world.bullet import Bullet

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
        self.lives = 3
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
