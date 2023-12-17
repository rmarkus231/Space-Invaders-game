import pygame as pg
import numpy as np

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