import pygame as pg
from .button import Button
import urllib.request
from .difficulty import Difficulty_screen
import webbrowser

class Main_menu(pg.sprite.Sprite):
    def __init__(self,w,h,timer):
        super().__init__()
        self.state = 0
        self.width = w
        self.height = h
        self.currentButton = None
        self.currentI = 0
        self.timer = timer
        img1 = "./graphics/buttons/start.png"
        img2 = "./graphics/buttons/quit.png"
        img3 = "./graphics/buttons/source.png"
        img4 = "./graphics/buttons/difficulty.png"
        """
        func1 = lambda : True
        func2 = lambda : pg.quit()
        func3 = lambda : urllib.request.urlopen('https://github.com/rmarkus231/Space-Invaders-game'), False
        func4 = lambda : print("Difficlty"),False
        """
        #1 = start, 2 = quit, 3 = open repo link, 4 = difficulty settings
        func1 = lambda : 1
        func2 = lambda : 2
        func3 = lambda : 3
        func4 = lambda : 4
        
        
        b1 = Button(self.width*1/3,self.width*1/3,img1,func1) # top left
        b2 = Button(self.width*2/3,self.width*1/3,img2,func2)  #top right
        b3 = Button(self.width*1/3,self.width*2/3,img3,func3) # bottom left
        b4 = Button(self.width*2/3,self.width*2/3,img4,func4)  #bottom right
        
        self.buttons = [b1,b2,b3,b4]
        self.difficulty_select = Difficulty_screen(w,h,self.timer)
        self.difficulty = 3
    
    def draw_base_menu(self,screen):
        #print(self.currentI,self.currentButton)
        for i,button in enumerate(self.buttons):
            self.buttons[i].draw(screen)
            button.currentButton = self.buttons[self.currentI]
            button.currentI = self.currentI
        
        #0 1
        #2 3
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT and self.currentI == 0:
                    self.currentI = 1
                elif event.key == pg.K_DOWN and self.currentI == 0:
                    self.currentI = 2
                elif event.key == pg.K_LEFT and self.currentI == 1:
                    self.currentI = 0
                elif event.key == pg.K_DOWN and self.currentI == 1:
                    self.currentI = 3
                elif event.key == pg.K_LEFT and self.currentI == 3:
                    self.currentI = 2
                elif event.key == pg.K_RIGHT and self.currentI == 2:
                    self.currentI = 3
                elif  event.key == pg.K_UP and self.currentI == 2:
                    self.currentI = 0
                elif  event.key == pg.K_UP and self.currentI == 3:
                    self.currentI = 1
                if event.key == pg.K_SPACE:
                    self.state = self.buttons[self.currentI].press()
        self.select(self.buttons[self.currentI])
    
    def draw(self,screen):
        if self.state in [0]:
            self.draw_base_menu(screen)
        elif self.state == 4:
            self.difficulty_select.draw(screen)
            if self.difficulty_select.state in [1,3,5]:
                self.difficulty = self.difficulty_select.state
                self.state = 0
                self.difficulty_select.state = 0
            elif self.difficulty_select.state == 9:
                self.state = 0
                self.difficulty_select.state = 0
        elif self.state == 3:
            print("opening URL")
            url = 'https://github.com/rmarkus231/Space-Invaders-game'
            webbrowser.open(url,new=0, autoraise=True)
            self.state = 0
        elif self.state == 2:
            pg.quit()
                
    def select(self,btn):
        self.currentButton = btn
            