import pygame as pg

class Button():
    select = False
    def __init__(self,x,y,image,func):
        self.currentButton = None
        self.currentI = 0
        self.img = image
        self.imgGray = image[0:-4]+"_bw.png"
        self.image = pg.image.load(self.img).convert_alpha()
        self.imageGray = pg.image.load(self.imgGray).convert_alpha()
        self.rect = self.image.get_rect( midbottom=(x,y) )
        self.callback =func
    
    def draw(self,screen):
        #pos = pg.mouse.get_pos()
        if self == self.currentButton:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.imageGray, (self.rect.x, self.rect.y))

    def press(self):
        self.callback()