import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
from game.game import Game
from game.menu.timer import Timer
#import time
# pygame setup
pg.init()

WIDTH = (600)        
HEIGHT = (600)

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Space Invaders")
clock = pg.time.Clock()
running = True
timer = Timer(50)
game = Game(WIDTH,HEIGHT,timer)

if __name__=="__main__":
    #create an appdata folder for high scores if doesnt exist
    path = os.path.expandvars(r'%APPDATA%\Space-invaders-game')
    pygame_icon = pg.image.load('graphics/player.png').convert_alpha()
    pg.display.set_icon(pygame_icon)
    if not os.path.exists(path):
        os.makedirs(path)
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        #tm = round(time.time()*1000,0)   #uses time import
        screen.fill("black")
        try:
            game.run(screen)
        
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            pg.display.flip()

            clock.tick(60)  # FPS limit
        except:
            running = False

    pg.quit()