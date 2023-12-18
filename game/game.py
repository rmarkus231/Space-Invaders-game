import pygame as pg
import random
from .enemy.aliens import Aliens
from .world.bullet import Bullet
from .world.defense import Defense
from .player.player import Player
from .menu.game_over import Game_over
from .menu.main_menu import Main_menu

class Game():
    #save window w/h to class local arg
    width = 0
    height = 0
    ready = False
    alien_cooldown = 1000 #in ms
    over = False
    startupCompleted = False
    def __init__(self,w,h):
        self.width = w
        self.height = h
        self.main_menu = Main_menu(self.width,self.height)
        p_sprite = Player((self.width/2 ,self.height))
        self.player = pg.sprite.GroupSingle(p_sprite)
        self.def_group = Defense(self.width,(10,self.height-50),10,100)
        self.aliens = Aliens(self.width,self.height,7,10,5,50,alien_speed= 1)
        #had to put the alien bullet group here because it would
        #NOT FUCKING DRAW if it was in the aliens class, POS
        self.alien_lasers = pg.sprite.Group()
        self.player_laser = pg.sprite.Group()
        self.time = pg.time.get_ticks()
        self.game_over = Game_over(self.width,self.height)
    
    
    def run(self,screen):
        if self.startupCompleted == False:
            self.startupCompleted = self.main_menu.done
            print(self.main_menu.done)
            self.main_menu.draw(screen)
        elif not self.over:
            self.alien_lasers.update()
            self.player_laser.update()
            self.aliens.update()
            self.player.update()
            
            self.over = self.collides()
            self.player_shoot()
            self.charge()
            if self.ready:
                self.alien_shoot()
                self.ready = False
                self.time = pg.time.get_ticks()
            
            self.def_group.shape_group.draw(screen)
            self.player.draw(screen)
            self.player_laser.draw(screen)
            self.aliens.aliens.draw(screen)
            self.alien_lasers.draw(screen)
        elif self.over:
            self.game_over.draw(screen)
    
    def collides(self):
        for b in self.player_laser:
            col = pg.sprite.spritecollide(b,self.def_group.shape_group,True)
            col2 = pg.sprite.spritecollide(b,self.aliens.aliens,True)
            if col or col2:
                b.kill()
                
        for ab in self.alien_lasers:
            col = pg.sprite.spritecollide(ab,self.def_group.shape_group,True)
            if col:
                if ab.clr != "yellow":
                    ab.kill()
            col = pg.sprite.spritecollide(ab,self.player,False) #needs to be false, otherwise it kills player sprite on collision
            if col:
                ab.kill()
                self.player.sprite.lives -= 1
                if self.player.sprite.lives < 0:
                    return True
        return False
    
    def alien_shoot(self):
        if self.aliens.aliens:
            a = random.choice(self.aliens.aliens.sprites())
            file = "./graphics/a_bullet_"+a.color+".png"
            self.alien_lasers.add(Bullet(a.rect.center,self.height,False,speed=-4, img = file,clr = a.color))
    
    def charge(self):
        if not self.ready:
            time = pg.time.get_ticks()
            if time -self.time > self.alien_cooldown:
                self.ready = True

    def player_shoot(self):
        k = pg.key.get_pressed()
        if k[pg.K_SPACE] and self.player.sprite.ready:
            self.player.sprite.ready = False
            self.player.sprite.time = pg.time.get_ticks()
            self.player_laser.add(Bullet(self.player.sprite.rect.center,0))