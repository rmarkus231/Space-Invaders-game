import pygame as pg
import cv2
import numpy as np

class Pixel(pg.sprite.Sprite):
    x = 0
    y = 0
    def __init__(self,x,y,color):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pg.Surface((1,1))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

class Defense(pg.sprite.Sprite):
    shape = []
    shape_group = None
    def __init__(self,width,pos,gaps,offset):
        super().__init__()
        self.img_2_shape()
        self.shape_group = pg.sprite.Group()
        """
        Uses numpy array as basis to make a group of pixels
        """
        #equal distribution of defensive 
        positions = np.linspace(
            0+offset/2,
            width-offset,
            num = gaps
            )
        #print(positions)
        
        for row_i,val1 in enumerate(self.shape):
            for col_i,val2 in enumerate(val1):
                if sum(val2) != 0:
                    #Since cv2 uses bgr and image is in rgp, swap b & r
                    val2[0], val2[2] = val2[2], val2[0]
                    clr = tuple(val2)
                    #print(clr)
                    for i,p in enumerate(positions):
                        #print(p)
                        self.shape_group.add(Pixel(
                            pos[0]+col_i+ p,
                            pos[1]+row_i,
                            clr))
    
    def img_2_shape(self):
        #converts image to numpy array
        self.shape = cv2.imread('graphics/barrier.png')
