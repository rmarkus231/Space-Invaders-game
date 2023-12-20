import pygame as pg
import random
from .enemy.aliens import Aliens, SpecialAlien
from .world.bullet import Bullet, AdvBullet
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
    special_alien_cooldown = 1500
    over = False
    startupCompleted = False
    
    def __init__(self,w,h,timer):
        self.width = w
        self.height = h
        self.timer = timer
        self.specialAlienActive = False
        self.sReady = False
        
        #world elements
        p_sprite = Player((self.width/2 ,self.height))
        self.player = pg.sprite.GroupSingle(p_sprite)
        self.def_group = Defense(self.width,(10,self.height-50),10,100)
        self.aliens = Aliens(self.width,self.height,7,10,5,50,alien_speed= 1)
        self.special = pg.sprite.GroupSingle(SpecialAlien(self.width,self.height))
        self.bounds = Bounds(w,h)
        self.UI = UI(w,h,self.player)

        #projectile groups
        self.alien_lasers = pg.sprite.Group()
        self.player_laser = pg.sprite.Group()
        
        #scenes
        self.main_menu = Main_menu(self.width,self.height,self.timer)
        self.game_over = Game_over(self.width,self.height,self.player)
        
        self.time = pg.time.get_ticks()
        self.stime = pg.time.get_ticks()
    
    
    def run(self,screen):
        if self.main_menu.state in [0,2,3,4]:
            self.main_menu.draw(screen)
        elif not self.over:
            if self.aliens.getAmount() == 0:
                #create new set of aliens for infinite gameplay
                #gets harder every loop
                self.aliens = Aliens(self.width,self.height,7,10,5,50,alien_speed= 1)
                self.main_menu.difficulty += 1
            self.get_difficulty(self.main_menu.difficulty) 
            self.alien_lasers.update()
            self.player_laser.update()
            self.aliens.update()
            self.player.update()
            self.UI.update()
            
            #actions for UFO
            self.callSpecialAlien()
            self.specialCharge()
            self.special.update()
            if self.specialAlienActive and self.special.sprite.inBounds():
                self.special.draw(screen)
                if self.sReady:
                    self.specialAlienShoot()
                    self.sReady = False
                    self.stime = pg.time.get_ticks()
            elif not self.special.sprite.inBounds():
                self.specialAlienActive = self.special.sprite.isGone()
                
            
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
    
    def callSpecialAlien(self):
        #self.aliens.special
        ran = random.randint(1,1000)
        if ran == 1 and not self.specialAlienActive:
            print("special alien activated")
            self.special.sprite.activate()
            ttl = random.randint(10000,25000)
            self.special.sprite.setTTL(ttl)
            self.specialAlienActive = True
            self.special.sprite.hit = False
    
    def collides(self): #this function returns true of game is over
        #actually used for more than collision, just general game state checking
        if self.aliens.current_aliens == 0:
            return True
        
        for b in self.player_laser:
            col = pg.sprite.spritecollide(b,self.def_group.shape_group,True)
            col2 = pg.sprite.spritecollide(b,self.aliens.aliens,True)
            col3 = pg.sprite.spritecollide(b,self.special, False)
            if col or col2:
                for el in col2:
                    self.player.sprite.score += self.get_score(el)
            if col3 and not self.special.sprite.hit:
                self.player.sprite.score += self.special.sprite.getScore()
                self.special.sprite.ttl = 0
                self.special.sprite.hit = True
            b.kill()

        #check if aliens collide with any wall
        if pg.sprite.groupcollide(self.aliens.aliens,self.bounds.left_wall,False,False) or pg.sprite.groupcollide(self.aliens.aliens,self.bounds.right_wall,False,False):
            self.aliens.alien_down()
        
        #check if an alien has touched any defenses, if so then its game over
        if pg.sprite.groupcollide(self.aliens.aliens,self.def_group.shape_group,False,False):
            return True
                
        for ab in self.alien_lasers:
            if pg.sprite.spritecollide(ab,self.def_group.shape_group,True):
                if ab.clr not in ["yellow","ufo"]:
                    ab.kill()
            if pg.sprite.spritecollide(ab,self.player,False): #needs to be false, otherwise it kills player sprite on collision
                ab.kill()
                self.player.sprite.lives -= 1
                self.UI.lives -= 1
                if self.player.sprite.lives < 0:
                    return True
        return False
    
    def specialAlienShoot(self):
        playerpos = [self.player.sprite.rect.x,-self.player.sprite.rect.y]
        #print(playerpos)
        file = "./graphics/lil_bullet.png"
        self.alien_lasers.add(AdvBullet(self.special.sprite.rect.center,self.height,False,speed=playerpos, img = file))

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

    def specialCharge(self):
        if not self.sReady:
            time = pg.time.get_ticks()
            if time -self.stime > self.special_alien_cooldown:
                self.sReady = True

    def player_shoot(self):
        k = pg.key.get_pressed()
        if k[pg.K_SPACE] and self.player.sprite.ready:
            self.special.sprite.increment()
            self.player.sprite.ready = False
            self.player.sprite.time = pg.time.get_ticks()
            self.player_laser.add(Bullet(self.player.sprite.rect.center,0))
    
    def get_score(self,alien):
        color = alien.color
        match color:
            case "purple":
                return 20*self.main_menu.difficulty
            case "yellow":
                return 30*self.main_menu.difficulty
            case "red":
                return 5*self.main_menu.difficulty
    
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