import pygame as pg
from classes import *
#import time
# pygame setup
pg.init()

WIDTH = (600)
HEIGHT = (600)

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
running = True
game = Game(WIDTH,HEIGHT)

if __name__=="__main__":
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        #tm = round(time.time()*1000,0)   #uses time import
        screen.fill("black")
        game.run(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.flip()

        clock.tick(60)  # FPS limit

    pg.quit()