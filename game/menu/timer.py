#this file makes sure menu inputs arent too rapid
import pygame as pg

class Timer():
    def __init__(self,t):
        self.ticks = lambda : pg.time.get_ticks()
        self.init_time = self.ticks()
        self.threshold = t
    
    def ready(self):
        if self.ticks() - self.init_time > self.threshold:
            self.init_time = self.ticks()
            return True
        else:
            return False