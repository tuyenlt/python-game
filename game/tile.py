import pygame
from game.settings import *

class Tile(pygame.sprite.Sprite):
    
    def __init__(self,pos, groups, image = None):
        super().__init__(groups)
        if image:
            self.image = image
            self.rect = self.image.get_rect(topleft = pos)
        else:
            (x, y) = pos
            self.rect = pygame.rect.Rect(x,y,TILE_SIZE, TILE_SIZE)
        self.hitbox = self.rect 