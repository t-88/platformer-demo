import pygame
import math
from enum import Enum
import globals as g
from  dotdict import *
from  collidable import *

PlayerAnimation = Enum("PlayerAnimation",["idle","jump","run"])
GRAVITY = 15
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100,100,48,64)
        self.acc = pygame.Vector2(0,0)
        self.vel = pygame.Vector2(0,0)
        self.dir = pygame.Vector2(0,0)
        self.vel_dir = pygame.Vector2(0,0)
        self.color = [255,255,255]
        
        self.fric = pygame.Vector2(-0.4,0)
        self.speed = 20
        self.max_speed = 40
        self.max_height = -80
        self.jump_force = -400
        
        
        self.grounded = False
        self.grounded_rect = pygame.Rect(0,0,10,10)
        
        
        self.took_damage = False
        self.invcble_timer = 0
        
        self.collidables = []
        self.spawner = None
        
        self.animation =    dotdict({
            "idx" : 0,
            "flipped": False,
            "dir_x": "right", 
            "typ": PlayerAnimation.idle,
            "frames":  {
                PlayerAnimation.idle : [pygame.transform.scale_by(pygame.image.load(f"assets/player/idle/player-idle-{i}.png").convert_alpha(),3) for i in range(1,5)],
                PlayerAnimation.jump : [pygame.transform.scale_by(pygame.image.load(f"assets/player/jump/player-jump-{i}.png").convert_alpha(),3) for i in range(1,3)],
                PlayerAnimation.run : [pygame.transform.scale_by(pygame.image.load(f"assets/player/run/player-run-{i}.png").convert_alpha(),3) for i in range(1,7)],
            },
            "sprite": None,
            "passed_time" : 0,
            "max_time" : 0.8,
            "changed" : False,
            })
        self.animation.sprite = self.animation.frames[PlayerAnimation.idle][0]
        
        
        self.hit_by_enemy = False
        self.hit_time = 0

        g.player = self
    def events(self):
        self.dir.x  = 0
        if g.keys[pygame.K_LEFT]:
            self.dir.x = -1
            self.animation.dir_x = "left"
        elif g.keys[pygame.K_RIGHT]:
            self.dir.x = 1
            self.animation.dir_x = "right"
            self.animation.typ = PlayerAnimation.run
            
        
        self.acc.x = self.dir.x * self.speed 

    
        if self.grounded and g.keys[pygame.K_SPACE] :
            self.acc.y += self.jump_force
            self.grounded = False
            
    
    def gravity(self):
        self.acc.y += GRAVITY
    
    
    def move(self):
        self.acc.x += self.vel.x * self.fric.x
        self.vel.x += self.acc.x  * g.dt
        if abs(self.vel.x) < 1:
            self.vel.x = 0 
        if not self.hit_by_enemy:
            if self.vel.x > 0:
                self.vel.x = min(self.vel.x,self.max_speed)
            else:
                self.vel.x = max(self.vel.x,-self.max_speed)
        else:
            self.hit_by_enemy = False
        self.rect.centerx += self.vel.x * g.dt 
        for collidable in self.collidables:
            if not collidable.collidable: continue

            if  collidable.rect.colliderect(self.rect):
                if self.vel.x > 0:
                    self.rect.right = collidable.rect.left
                else:
                    self.rect.x = collidable.rect.right 


        self.grounded = False


        self.vel.y += self.acc.y * g.dt
        if not self.hit_by_enemy:
            if self.vel.y < 0:
                self.vel.y = max(self.vel.y,self.max_height)
        else:
            self.hit_by_enemy = False        
        self.rect.centery += self.vel.y * g.dt 
        
        self.grounded_rect.centerx = self.rect.centerx
        self.grounded_rect.centery = self.rect.bottom 
        for collidable in self.collidables:
            if not collidable.collidable: continue
            
            if collidable.rect.colliderect(self.rect) :
                if self.vel.y > 0 and collidable.collide_skip_dir != CollideDir.Down:
                    self.rect.bottom = collidable.rect.y
                    self.grounded = True
                    self.vel.y = 0
                elif self.vel.y < 0: 
                    if collidable.collide_skip_dir != CollideDir.Up:
                        self.rect.top = collidable.rect.bottom
                        self.vel.y = 0
                    else:
                        collidable.collidable = False
            if self.grounded_rect.colliderect(collidable.rect):
                if self.vel.y > 0:
                    self.grounded = True

            
                

    def collide_enemies(self):
        if self.took_damage: return
        
        y = self.rect.y
        self.rect.y += self.vel.y * g.dt 
        for collidable in self.spawner.enemies:
            if collidable.destroy: continue
            if collidable.rect.colliderect(self.rect) :
                if self.vel.y > 0 and self.rect.top < collidable.rect.top:
                    self.vel.y = 0 
                    self.acc.y = -300 
                    collidable.destroy = True
                elif self.vel.y < 0 and self.rect.bottom >= collidable.rect.bottom:
                    self.took_damage = True
                    self.vel.y = 0 

        self.rect.y = y

        x = self.rect.x        
        self.rect.x += self.vel.x * g.dt
        
        if self.took_damage: return
        for collidable in self.spawner.enemies:
            if collidable.destroy: continue
                 
            if collidable.rect.colliderect(self.rect) :
                self.took_damage = True
                self.hit_by_enemy = True
                self.rect.left = collidable.rect.right
                
                self.vel.x = 0
                self.vel.y = 0
                
                self.acc.y = -300
                self.acc.x = collidable.dir.x * 500
                break
        self.rect.x = x
        
    
    def anim(self):
        if self.grounded:
            if self.dir.x == 0:
                if self.animation.typ != PlayerAnimation.idle:
                    self.animation.typ = PlayerAnimation.idle
                    self.animation.idx = 0
                    self.animation.changed = True
            else:
                if self.animation.typ != PlayerAnimation.run:
                    self.animation.typ = PlayerAnimation.run
                    self.animation.idx = 0
                    self.animation.changed = True
                    
        else:
            if self.animation.typ != PlayerAnimation.jump:
                self.animation.typ = PlayerAnimation.jump
                self.animation.changed = True
                
        if self.animation.typ == PlayerAnimation.jump:
            if self.vel.y < 0:
                self.animation.idx = 1
                self.animation.changed = True
            else:
                self.animation.idx = 0
                self.animation.changed = True
                            
                    
        if self.animation.typ != PlayerAnimation.jump or self.animation.changed:
            if self.animation.passed_time > self.animation.max_time:
                self.animation.idx = (self.animation.idx + 1) % len(self.animation.frames[self.animation.typ]) 
                self.animation.sprite = self.animation.frames[self.animation.typ][self.animation.idx].copy()
                
                self.animation.passed_time = 0
                if self.animation.dir_x == "left":
                    self.animation.sprite = pygame.transform.flip(self.animation.sprite,True,False)
                self.animation.changed = False

                return
            self.animation.passed_time += g.dt
    def invincible(self):
        if not self.took_damage: return
        if self.invcble_timer < 15:
            self.invcble_timer += g.dt
            return
        self.invcble_timer = 0
        self.took_damage = False
            
    def update(self):
        self.acc.x = 0
        self.acc.y = 0
        
        
        self.events()
        self.gravity()
        self.invincible()
        self.collide_enemies()
        self.move()
        self.anim()

                

    
    def render(self):
        # pygame.draw.rect(g.display,self.color,self.rect)
        # pygame.draw.rect(g.display,(255,0,0),self.grounded_rect)
        if self.took_damage:
            self.animation.sprite.fill((255,255,255,220) ,None,pygame.BLEND_RGBA_MULT)
        g.display.blit(
                self.animation.sprite,(self.rect.x - 25,self.rect.y - 30)
        )