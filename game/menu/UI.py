import pygame as pg
from .button import Icon

class UI(pg.sprite.Sprite):
    score = 0
    def __init__(self,w,h,player):
        super().__init__()
        self.width = w
        self.height = h
        self.padding = 20
        self.player_image = "./graphics/player.png"
        
        #player is a singlegroup, containing player sprite
        self.player = player.sprite
        self.lives = self.player.lives
        self.lives_indicator = []
        
        self.initLives()
        
    def draw(self,screen):
        screen.blit(self.scoreDisp,(self.scoreRect.x,self.scoreRect.y))
        
        for life in self.lives_indicator:
            life.draw(screen)
        
        
    def update(self):
        self.putScore()
        self.checkHit()
    
    def checkHit(self):
        if self.lives < len(self.lives_indicator):
            print("deleted life")
            del self.lives_indicator[-1]
    
    def initLives(self):
        #player size is 32x32
        for i in range(self.lives):
            x = self.padding + i*(32+10)
            self.lives_indicator.append(Icon(x,self.padding,self.player_image))
    
    def putScore(self):
        #score display
        self.score = str(self.player.score)
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.scoreDisp = self.font.render(self.score, False,(255,255,255))
        
        self.scoreRect = self.scoreDisp.get_rect( topright = (self.width-self.padding,self.padding))
        