import pygame as pg
import random
from .enemy.aliens import Aliens
from .world.bullet import Bullet
from .world.defense import Defense
from .player.player import Player
from .menu.game_over import Game_over
from .menu.main_menu import Main_menu
from .world.bounds import Bounds
from .menu.UI import UI

class Game():
    #save window w/h to class local arg
    width = 0
    height = 0
    ready = False
    alien_cooldown = 1000 #in ms
    over = False
    startupCompleted = False
    
    def __init__(self,w,h,timer):
        self.width = w
        self.height = h
        self.timer = timer
        
        #scenes
        self.main_menu = Main_menu(self.width,self.height,self.timer)
        self.game_over = Game_over(self.width,self.height)
        
        #world elements
        p_sprite = Player((self.width/2 ,self.height))
        self.player = pg.sprite.GroupSingle(p_sprite)
        self.def_group = Defense(self.width,(10,self.height-50),10,100)
        self.aliens = Aliens(self.width,self.height,7,10,5,50,alien_speed= 1)
        self.bounds = Bounds(w,h)
        self.UI = UI(w,h,self.player)

        #projectile groups
        self.alien_lasers = pg.sprite.Group()
        self.player_laser = pg.sprite.Group()
        
        self.time = pg.time.get_ticks()
    
    
    def run(self,screen):
        if self.main_menu.state in [0,2,3,4]:
            self.main_menu.draw(screen)
        elif not self.over:
            self.get_difficulty(self.main_menu.difficulty) 
            self.alien_lasers.update()
            self.player_laser.update()
            self.aliens.update()
            self.player.update()
            self.UI.update()
            
            self.over = self.collides()
            self.player_shoot()
            self.charge()
            if self.ready:
                self.alien_shoot()
                self.ready = False
                self.time = pg.time.get_ticks()
            
            self.def_group.shape_group.draw(screen)
            self.UI.draw(screen)
            self.player.draw(screen)
            self.player_laser.draw(screen)
            self.aliens.aliens.draw(screen)
            self.alien_lasers.draw(screen)
            self.bounds.draw(screen)
        elif self.over:
            self.game_over.draw(screen)
    
    def collides(self): #this function returns true of game is over
        #actually used for more than collision, just general game state checking
        if self.aliens.current_aliens == 0:
            return True
        
        for b in self.player_laser:
            col = pg.sprite.spritecollide(b,self.def_group.shape_group,True)
            col2 = pg.sprite.spritecollide(b,self.aliens.aliens,True)
            if col or col2:
                for el in col2:
                    self.player.sprite.score += self.get_score(el)
                b.kill()
        
        #check if aliens collide with any wall
        if pg.sprite.groupcollide(self.aliens.aliens,self.bounds.left_wall,False,False) or pg.sprite.groupcollide(self.aliens.aliens,self.bounds.right_wall,False,False):
            self.aliens.alien_down()
        
        #check if an alien has touched any defenses, if so then its game over
        if pg.sprite.groupcollide(self.aliens.aliens,self.def_group.shape_group,False,False):
            return True
                
        for ab in self.alien_lasers:
            if pg.sprite.spritecollide(ab,self.def_group.shape_group,True):
                if ab.clr != "yellow":
                    ab.kill()
            if pg.sprite.spritecollide(ab,self.player,False): #needs to be false, otherwise it kills player sprite on collision
                ab.kill()
                self.player.sprite.lives -= 1
                self.UI.lives -= 1
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
    
    def get_score(self,alien):
        color = alien.color
        match color:
            case "purple":
                return 50
            case "yellow":
                return 100
            case "red":
                return 20
    
    def get_difficulty(self,dif):
        #levels are
        #1,3,5
        match dif:
            case 1:
                self.alien_cooldown = 1500
                self.aliens.dif = 1
            case 3:
                self.alien_cooldown = 1000
                self.aliens.dif = 3
            case 5:
                self.alien_cooldown = 500
                self.aliens.dif = 5