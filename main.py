import pygame
import globals as g
from player import *
from enemy_spawner import *
from collidable import *
from passthrough_collidable import *
from sprite import *


pygame.init()
g.display = pygame.display.set_mode((g.WIDTH,g.HEIGHT))
g.clock = pygame.time.Clock()
g.load_sprites()





player = Player()
spawner = EnemySpawner()
player.spawner = spawner


collidables = [
    # horz top floor
    Collidable(0,32 * 12,32 * 24,32),
    Collidable(32 * 28,32 * 12,32 * 2,32),

    # horz bottom
    Collidable(0,32 * 15,32 * 24,32),
    Collidable(32 * 28,32 * 15,32 * 1,32),
    Collidable(32 * 1,32 * 24,32 * 27,32 * 6),


    # vert ceil
    Collidable(32 * 23,32 * 13,32,32 * 2),
    Collidable(32 * 28,32 * 13,32,32 * 2),

    # vert bottom
    Collidable(32 * 28,32 * 16,32,32 * 8),
    Collidable(32 * 0,32 * 16,32,32 * 8),


    # vert border
    Collidable(32 * -1,0,32,32 * 11),
    Collidable(32 * 30,0,32,32 * 11),

    PassThroughCollidable(32 * 24,32 * 12,32 * 4,16),
    PassThroughCollidable(32 * 24,32 * 16,32 * 4,16),
    PassThroughCollidable(32 * 24,32 * 20,32 * 4,16),
]
player.collidables = collidables


env_sprites = []
env_sprites.append(Sprite(0,0,"map"))


print("JUMPING is fps dependent, sorry ;)")

g.dt = 0
running = True
while running:
    g.dt = g.clock.tick(60) / 100
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
          if e.key == pygame.K_ESCAPE:
                running = False

    g.keys = pygame.key.get_pressed()

    
    
    for collidable in collidables:
        collidable.update()
    
    
    spawner.update()
    player.update()
    
    
    for sprite in env_sprites:
        sprite.render()
    # for collidable in collidables:
        # collidable.render()
    player.render()
    spawner.render()



    pygame.display.flip()
    g.display.fill((112,227,206))


pygame.quit()