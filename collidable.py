import pygame
from enum import Enum
import globals as g

CollideDir = Enum("CollideDir",["Up","Down","Left","Right","Null"])

class Collidable:
    def __init__(self,x,y,w,h,color=(255,255,0)): 
        self.rect = pygame.Rect(x,y,w,h)
        self.collidable = True
        self.collide_skip_dir = CollideDir.Null
        self.color = color

    def update(self):
        pass
    def render(self):
        pygame.draw.rect(g.display,self.color,self.rect)