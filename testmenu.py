import pygame as pg
from game.menu.button import Button

class TestMenu(pg.sprite.Sprite):
    def __init__(self,w,h):
        super().__init__()
        self.width = w
        self.height = h
        self.currentButton = None
        self.currentI = 0
        img = "./graphics/btn.png"
        
        func1 = lambda : print("top left pressed")
        func2 = lambda : print("top right pressed")
        func3 = lambda : print("bottom left pressed")
        func4 = lambda : print("bottom right pressed")
        
        b1 = Button(self.width*1/3,self.width*1/3,img,func1) # top left
        b2 = Button(self.width*2/3,self.width*1/3,img,func2)  #top right
        b3 = Button(self.width*1/3,self.width*2/3,img,func3) # bottom left
        b4 = Button(self.width*2/3,self.width*2/3,img,func4)  #bottom right
        self.buttons = [b1,b2,b3,b4]
    
    def draw(self,screen):
        k = pg.key.get_pressed()
        #print(self.currentI,self.currentButton)
        for i,button in enumerate(self.buttons):
            self.buttons[i].draw(screen)
            button.currentButton = self.buttons[self.currentI]
            button.currentI = self.currentI
        
        #0 1
        #2 3
        
        if k[pg.K_RIGHT] and self.currentI == 0:
            self.currentI = 1
        elif k[pg.K_DOWN] and self.currentI == 0:
            self.currentI = 2
        elif k[pg.K_LEFT] and self.currentI == 1:
            self.currentI = 0
        elif k[pg.K_DOWN] and self.currentI == 1:
            self.currentI = 3
        elif k[pg.K_LEFT] and self.currentI == 3:
            self.currentI = 2
        elif k[pg.K_RIGHT] and self.currentI == 2:
            self.currentI = 3
        elif  k[pg.K_UP] and self.currentI == 2:
            self.currentI = 0
        elif  k[pg.K_UP] and self.currentI == 3:
            self.currentI = 1
        
        if k[pg.K_SPACE]:
            self.done = self.buttons[self.currentI].press()
        self.select(self.buttons[self.currentI])
        
    def select(self,btn):
        self.currentButton = btn
        
    


pg.init()

WIDTH = (600)
HEIGHT = (600)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Invaders")
clock = pg.time.Clock()
running = True
game = TestMenu(WIDTH,HEIGHT)

if __name__=="__main__":
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        #tm = round(time.time()*1000,0)   #uses time import
        screen.fill("black")
        game.draw(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.flip()

        clock.tick(60)  # FPS limit

    pg.quit()