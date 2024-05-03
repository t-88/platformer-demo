import pygame
import globals as g
from  dotdict import *


class Enemy:
    def __init__(self, x , y):
        self.rect = pygame.Rect(x,y,48,94)
        self.color = [255,255,255]
        self.destroy = False
        
        
        
        self.animation =    dotdict({})
        self.animation.sprite = None 
        
        
        self.dir = pygame.Vector2(0,0)

    
    
    def update(self):
        pass
        
    def render(self):
        pygame.draw.rect(g.display,self.color,self.rect)