import pygame as pg
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