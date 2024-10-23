import pygame
from game.settings import *
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self,firing_pos,angle,groups, owner):
        super().__init__(groups)
        self.image = pygame.image.load("./assets/images/bullet.png").convert_alpha()
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rect = self.image.get_rect(center = firing_pos)
        self.hitbox = self.rect.inflate((0,12))
        self.speed = 40
        self.x_vel = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_vel = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.owner = owner
        
    def movement(self):
        self.rect.centerx += int(self.x_vel)
        self.rect.centery += int(self.y_vel)
        self.hitbox.center = self.rect.center
        
    def collition(self, sprites_groups):
        for sprite in sprites_groups:
            if self.hitbox.colliderect(sprite.rect):
                self.kill()
    
    def update(self):
        self.movement()

        