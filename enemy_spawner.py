from bunny import *
from ghost import *
from random import randint

class EnemySpawner:
    def __init__(self):
        self.enemies = [
        ]
        
        
        self.bunny_count = 0
        self.ghost_count = 0
        
        
    
    def update(self):
        for i in range(len(self.enemies) - 1, -1 , -1):
            self.enemies[i].update()
            if self.enemies[i].destroy:
                if type(self.enemies[i]) == Bunny: self.bunny_count = 0
                else: self.ghost_count = 0
                self.enemies.pop(i)
                



        
        if self.bunny_count == 0:
            self.bunny_count = 1
            if randint(0,100) > 50:
                self.enemies.append(Bunny(-32 * 2,32 * 9,1))
            else:
                self.enemies.append(Bunny(g.WIDTH + 32,32 * 9,-1))
        
        if self.ghost_count == 0:
            self.ghost_count = 1
            
            
            self.enemies.append(Ghost(0,32 * 18))
                            
    
    def render(self):
        for enemy in self.enemies:
            enemy.render()
            

    