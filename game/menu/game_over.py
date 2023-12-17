import pygame as pg

class button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect( midbottom=(x,y) )
    
    def draw(self,screen):
        pos = pg.mouse.get_pos()
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for event in pg.event.get():
            #if self.rect.collidepoint(pos) and event.type==pg.KEYDOWN and event.key==pg.K_LEFT:
            #    pg.quit()
            if event.type==pg.KEYDOWN and event.key==pg.K_SPACE:
                pg.quit()
            

class Game_over(pg.sprite.Sprite):
    def __init__(self,w,h):
        super().__init__()
        self.width = w
        self.height = h
        img = pg.image.load("./graphics/game_over.png").convert_alpha()
        self.button = button(self.width/2,self.width/2,img)
    
        
        