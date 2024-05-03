import pygame
import globals as g
from collidable import *

class PassThroughCollidable(Collidable):
    def __init__(self,x,y,w,h): 
        super().__init__(x,y,w,h)
        self.rect = pygame.Rect(x,y,w,h)
        self.collide_skip_dir = CollideDir.Up
    
    def update(self):
        if self.collidable:
            if g.keys[pygame.K_DOWN]:
                self.collidable = False
        elif not g.keys[pygame.K_DOWN] and not self.rect.colliderect(g.player.rect):
            self.collidable = True
                
    def render(self):
        pygame.draw.rect(g.display,[255,0,0],self.rect)