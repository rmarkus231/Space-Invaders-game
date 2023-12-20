import pygame as pg
from .button import Button
import os
import sys

def restart():
    try:
        os.execv(sys.executable, ['py'] + sys.argv)
    except:
        os.execv(sys.executable, ['python3'] + sys.argv)

class Game_over(pg.sprite.Sprite):
    def __init__(self,w,h,player):
        super().__init__()
        self.width = w
        self.height = h
        self.currentButton = None
        self.currentI = 0
        img = "./graphics/buttons/quit.png"
        img2 = "./graphics/buttons/restart.png"
        self.gotScore = False
        #to make sure that you dont missclick exit by holding spacebar while you die
        self.madeTimer = False
        #make sure you write to file only once since you dont want
        #to be doing constant i/o calls while sitting at end screen
        self.writtenScore = False
        
        self.scoreFile = os.path.expandvars(r'%APPDATA%\Space-invaders-game\\highscore.txt')
        
        func = lambda : pg.quit()
        func2 = lambda : restart()
        b = Button(self.width*1/3,self.width/2,img,func)
        b2 = Button(self.width*2/3,self.width/2,img2,func2)
        self.player = player.sprite
        self.buttons = [b,b2]
        
    def draw(self,screen):
        self.score = int(self.player.score)
        if not self.madeTimer:
            #make timer
            self.initLoadTime = pg.time.get_ticks()
            self.madeTimer = True
        
        
        k = pg.key.get_pressed()
        #button functionality segment
        for i,button in enumerate(self.buttons):
            self.buttons[i].draw(screen)
            button.currentButton = self.buttons[self.currentI]
            button.currentI = self.currentI
        if k[pg.K_RIGHT] and self.currentI == 0:
            self.currentI = 1
        elif k[pg.K_LEFT] and self.currentI == 1:
            self.currentI = 0
        if abs(self.initLoadTime - pg.time.get_ticks()) > 1000:
            if k[pg.K_SPACE]:
                self.status = self.buttons[self.currentI].press()
            self.select(self.buttons[self.currentI])
        
        if not self.gotScore:
            self.getHighscore()
        if not self.writtenScore:
            self.putHighscore()
        self.putScore()
        screen.blit(self.scoreDisp,(self.scoreRect.x,self.scoreRect.y))
        screen.blit(self.highScoreDisp,(self.highScoreRect.x,self.highScoreRect.y))
            
    def putScore(self):
        #score display
        self.font = pg.font.Font('freesansbold.ttf', 32)
        txt = f"Score: {self.score}"
        self.scoreDisp = self.font.render(txt, False,(255,255,255))
        self.scoreRect = self.scoreDisp.get_rect( midbottom = (self.width*1/2,self.width*8/12))
        
        hTxt = f"High score: {self.highScore}"
        self.highScoreDisp = self.font.render(hTxt, False,(255,255,255))
        self.highScoreRect = self.highScoreDisp.get_rect( midbottom = (self.width*1/2,self.width*10/12))
    
    def select(self,btn):
        self.currentButton = btn
    
    def getHighscore(self):
        #gets high score from file if exists, if doesnt exist, makes new file
        try:
            with open(self.scoreFile,"r",encoding = "UTF-8") as file:
                fr = file.readlines()[0]
                try:
                    lineClean = int(fr)
                    print("found highscore",str(lineClean))
                except:
                    print("line in file couldnt be got")
                    lineClean = 0
                self.highScore = lineClean
        except:
            with open(self.scoreFile,"w") as f:
                "couldnt find file"
                self.highScore = 0
        self.gotScore = True
    
    def putHighscore(self):
        with open(self.scoreFile,"w",encoding = "UTF-8") as file:
            print("Saving to file")
            if self.highScore < self.score:
                self.highScore = self.score
            file.write(str(self.highScore))
        self.writtenScore = True
        
        