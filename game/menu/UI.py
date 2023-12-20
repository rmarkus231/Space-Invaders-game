import pygame as pg
from .button import Icon
import os

class UI(pg.sprite.Sprite):
    score = 0
    def __init__(self,w,h,player):
        super().__init__()
        self.width = w
        self.height = h
        self.padding = 20
        self.player_image = "./graphics/player.png"
        
        self.scoreFile = os.path.expandvars(r'%APPDATA%\Space-invaders-game\\highscore.txt')
        
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
        txt = f"Score: {self.score}"
        self.scoreDisp = self.font.render(txt, False,(255,255,255))
        
        self.scoreRect = self.scoreDisp.get_rect( topright = (self.width-self.padding,self.padding))
    
    def getHighscore(self):
        #gets high score from file if exists, if doesnt exist, makes new file
        if os.path.exist(self.scoreFile,"r",encoding = "UTF-8"):
            with open(self.scoreFile) as file:
                fr = file.readline(0)
                #just incase someone writes a non number in the file
                try:
                    lineClean = int(fr.strip())
                except:
                    lineClean = 0
                self.highScore = lineClean
        else:
            with open(self.scoreFile,"w") as f:
                self.highScore = 0
        