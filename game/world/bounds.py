import pygame as pg

class Wall(pg.sprite.Sprite):
    def __init__(self,x,y,):
        super().__init__()
        self.image = pg.image.load("./graphics/wall.png")
        self.rect = self.image.get_rect( topleft = (x,y))

class Bounds(object):
    def __init__(self,w,h):
        self.width = w
        self.height = h
        wall_thickness = 3
        
        wall1 = Wall(0,0)
        wall2 = Wall(self.width-wall_thickness,0,)
        
        self.left_wall = pg.sprite.GroupSingle(wall1)
        self.right_wall = pg.sprite.GroupSingle(wall2)
    
    def draw(self,screen):
        self.left_wall.draw(screen)
        self.right_wall.draw(screen)
    