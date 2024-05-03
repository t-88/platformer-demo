import pygame
from enum import Enum
import globals as g
from  dotdict import *
from  enemy import *
from  collidable import *
import math


GhostAnimation = Enum("GhostAnimation",["fly"])

class Ghost(Enemy):
    def __init__(self, x , y) -> None:
        super().__init__(x,y)
        self.animation =    dotdict({
            "idx" : 0,
            "typ": GhostAnimation.fly,
            "frames":  {
                GhostAnimation.fly : [pygame.transform.scale_by(pygame.image.load(f"assets/ghost/fly/{i}.png").convert_alpha(),2.6) for i in range(1,7)],
            },
            "sprite": None,
            "passed_time" : 0,
            "max_time" : 0.8,
            })
        self.animation.sprite = self.animation.frames[self.animation.typ][0]
        self.rect.w = 48
        self.rect.h =  64
        
        self.start_y = y
        self.xdir = 1

    
    
    def anim(self):
        if self.animation.passed_time > self.animation.max_time:
            self.animation.passed_time = 0
            self.animation.idx = (self.animation.idx + 1) % len(self.animation.frames[self.animation.typ]) 
            self.animation.sprite = self.animation.frames[self.animation.typ][self.animation.idx]
            if self.xdir == -1:
                self.animation.sprite = pygame.transform.flip(self.animation.sprite,True,False)
            return


        self.animation.passed_time += g.dt
    def update(self):
        self.anim()
        self.rect.y = self.start_y + math.sin(pygame.time.get_ticks() / 1000 ) * 100 
        self.rect.x += self.xdir * 15 * g.dt 
        
        
        if  self.xdir == 1 and self.rect.right > g.WIDTH:
            self.xdir = -1
        elif self.xdir == -1 and self.rect.left < 0 :
            self.xdir = 1
            
        
    def render(self):
        g.display.blit(
                self.animation.sprite,(self.rect.x - 54,self.rect.y - 54  )
        )        