import pygame as pg
from .button import Button

class Game_over(pg.sprite.Sprite):
    def __init__(self,w,h):
        super().__init__()
        self.width = w
        self.height = h
        self.currentButton = None
        self.currentI = 0
        img = "./graphics/buttons/quit.png"
        img2 = "./graphics/buttons/restart.png"
        func = lambda : pg.quit()
        func2 = lambda : print("restart")
        b = Button(self.width*1/3,self.width/2,img,func)
        b2 = Button(self.width*2/3,self.width/2,img2,func2)
        self.buttons = [b,b2]
        
    def draw(self,screen):
        k = pg.key.get_pressed()
        #print(self.currentI)
        for i,button in enumerate(self.buttons):
            self.buttons[i].draw(screen)
            button.currentButton = self.buttons[self.currentI]
            button.currentI = self.currentI
        if k[pg.K_RIGHT] and self.currentI == 0:
            self.currentI = 1
        elif k[pg.K_LEFT] and self.currentI == 1:
            self.currentI = 0
        if k[pg.K_SPACE]:
            self.buttons[self.currentI].press()
        self.select(self.buttons[self.currentI])
            
    
    def select(self,btn):
        self.currentButton = btn
    
        
        