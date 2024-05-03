import pygame
import globals as g

class Sprite:
    def __init__(self,x,y,sprite_id):
        self.x = x
        self.y = y
        self.sprite_id = sprite_id
    
    def render(self):
        g.display.blit(g.sprites[self.sprite_id],(self.x,self.y))