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
        print("alien speed:",self.alien_speed)
        self.aliens.update(self.alien_speed)
    
    def alien_down(self):
        self.alien_direction *= -1
        for a in self.aliens:
            a.rect.y += abs(self.alien_speed*3)
        self.update()
    
    def set_difficulty(self,new):
        self.dif = new
                
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