from dotdict import *
import globals as g
import pygame

TILE_SIZE = 32
WIDTH = TILE_SIZE * 30
HEIGHT = TILE_SIZE * 25

display = None
clock = None
keys = []
dt = 0
player = None
tileset_sheet = None

sprites = dotdict({
    "map" : "assets/map.png"    
})


def create_sprite(pos):
    sprite = pygame.Surface((16,16)).convert()
    sprite.blit(tileset_sheet,(0,0),(16 * pos[0],16 * pos[1],16,16))
    sprite = pygame.transform.scale_by(sprite,2)
    return sprite

def load_sprites():
    sprites.map = pygame.transform.scale_by(pygame.image.load(sprites.map),2)
     
    
        
    