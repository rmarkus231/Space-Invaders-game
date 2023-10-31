import pygame as pg
from classes import *
#import time
# pygame setup
pg.init()
screen = pg.display.set_mode((800, 600))
clock = pg.time.Clock()
running = True

r_x = 300
r_y = 300
b_trigger = False
d_trigger = False

bullets = []
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    #tm = round(time.time()*1000,0)   #uses time import
    screen.fill("black")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if event.type == pg.KEYDOWN:
        if event.key == pg.K_RIGHT:
            r_x += 5
        if event.key == pg.K_LEFT:
            r_x -= 5
    rect = pg.draw.rect(screen, (0,255,0), (r_x,r_y,50,20))
    
    tm = pg.time.get_ticks()
    #print(tm)
    if not bool(tm % 20) and b_trigger:
        b_trigger == False
        b = bullet(r_x,r_y,5,20,500)
        bullets.append(b)
    else:
        b_trigger = True
     
    print(len(bullets))
    
    tm = pg.time.get_ticks()
    for b in bullets:
        b.update_params(b.x,b.y - 5,b.w,b.h)
        b.draw(screen)
    
    if not bool(tm % 100) and d_trigger and len(bullets) > 5:
        del bullets[0:5]
        d_trigger = False
    else:
        d_trigger = True
    
    
    # fill the screen with a color to wipe away anything from last frame
    
    

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pg.display.flip()

    clock.tick(60)  # limits FPS to 60

pg.quit()