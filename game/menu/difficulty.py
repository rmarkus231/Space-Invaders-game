import pygame as pg
from .button import Button

class Difficulty_screen(pg.sprite.Sprite):
    def __init__(self,w,h,timer):
        super().__init__()
        self.state = 0
        self.width = w
        self.height = h
        self.currentButton = None
        self.currentI = 0
        self.oldI = 0
        self.timer = timer
        
        img1 = "./graphics/buttons/low.png"
        img2 = "./graphics/buttons/mid.png"
        img3 = "./graphics/buttons/high.png"
        img4 = "./graphics/buttons/back.png"
        
        """
        func1 = lambda : True
        func2 = lambda : pg.quit()
        func3 = lambda : urllib.request.urlopen('https://github.com/rmarkus231/Space-Invaders-game'), False
        func4 = lambda : print("Difficlty"),False
        """
        
        #1 = easy mode multiplier
        #2 = normal mode multiplier
        #3 = hard mode multiplier
        #0 = back to main menu
        func1 = lambda : 1
        func2 = lambda : 3
        func3 = lambda : 5
        func4 = lambda : 9
                
        b1 = Button(self.width*1/4,self.width*1/3,img1,func1) # top left
        b2 = Button(self.width*2/4,self.width*1/3,img2,func2)  #top right
        b3 = Button(self.width*3/4,self.width*1/3,img3,func3) # bottom left
        b4 = Button(self.width*1/2,self.width*2/3,img4,func4)  #bottom right
        
        self.buttons = [b1,b2,b3,b4]

    def draw(self,screen):
        k = pg.key.get_pressed()
        #print(self.currentI,self.currentButton)
        for i,button in enumerate(self.buttons):
            self.buttons[i].draw(screen)
            button.currentButton = self.buttons[self.currentI]
            button.currentI = self.currentI
        
        #0 1 2
        #  3
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT and self.currentI == 0:
                    self.currentI = 1
                elif event.key == pg.K_DOWN and self.currentI == 0:
                    self.oldI = 0
                    self.currentI = 3
                elif event.key == pg.K_LEFT and self.currentI == 1:
                    self.currentI = 0
                elif event.key == pg.K_RIGHT and self.currentI == 1:
                    self.currentI = 2
                elif event.key == pg.K_DOWN and self.currentI == 1:
                    self.oldI = 1
                    self.currentI = 3
                elif  event.key == pg.K_DOWN and self.currentI == 2:
                    self.oldI = 2
                    self.currentI = 3
                elif  event.key == pg.K_LEFT and self.currentI == 2:
                    self.currentI = 1
                elif  event.key == pg.K_UP and self.currentI == 3:
                    self.currentI = self.oldI
                if event.key == pg.K_SPACE:
                    self.state = self.buttons[self.currentI].press()
            self.select(self.buttons[self.currentI])
    
    def select(self,btn):
        if self.timer.ready():
            self.currentButton = btn
            