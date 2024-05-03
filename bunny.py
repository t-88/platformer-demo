import pygame
from enum import Enum
import globals as g
from  dotdict import *
from  enemy import *
from  collidable import *


BunnyAnimation = Enum("BunnyAnimation",["run"])

class Bunny(Enemy):
    def __init__(self, x , y,dirx) -> None:
        super().__init__(x,y)
        self.animation =    dotdict({
            "idx" : 0,
            "typ": BunnyAnimation.run,
            "frames":  {
                BunnyAnimation.run : [pygame.transform.scale_by(pygame.image.load(f"assets/bunny/run/{i}.png").convert_alpha(),3) for i in range(1,7)],
            },
            "sprite": None,
            "passed_time" : 0,
            "max_time" : 0.8,
            })
        self.animation.sprite = self.animation.frames[self.animation.typ][0]

        self.dir.x = dirx
    
    def anim(self):
        if self.animation.passed_time > self.animation.max_time:
            self.animation.passed_time = 0
            self.animation.idx = (self.animation.idx + 1) % len(self.animation.frames[self.animation.typ]) 
            self.animation.sprite = self.animation.frames[self.animation.typ][self.animation.idx]
            if self.dir.x < 0:
                self.animation.sprite = pygame.transform.flip(self.animation.sprite,True,False)
            return


        self.animation.passed_time += g.dt
    def update(self):
        self.anim()
        self.rect.move_ip(5 * self.dir.x,0)
        if self.dir.x > 0 and self.rect.left > g.WIDTH:
            self.destroy = True
        elif self.dir.x < 0 and self.rect.right < 0:
            self.destroy = True
            
    def render(self):
        # super().render()
        g.display.blit(
                self.animation.sprite,(self.rect.x - 25,self.rect.y - 30)
        )        