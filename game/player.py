import pygame
import math
import os

from game.settings import *
from game.ultis.resource_loader import *

class Player(pygame.sprite.Sprite):
    
    def __init__(self, spwan_pos, sprite_groups, obtacles_sprites, team = "ct", id = "tuyenlt"):
        super().__init__(sprite_groups)
        #* display init
        self.org_image = get_tile_texture(f'./assets/player/{team}1.bmp', 0, 64)
        self.image = self.org_image
        self.obtacles_sprites = obtacles_sprites
        self.rect = self.image.get_rect(topleft = spwan_pos)
        self.hitbox = self.rect
        self.team = team
        self.id = id
        
        #* attr init
        self.angle = 0
        self.direction = pygame.math.Vector2()
        self.speed = 10
        self.bullets_sprites = []
    
    def handle_key_input(self):
        keys = pygame.key.get_pressed()
        
        #********** movement input
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0 
        #********** end movement input
        
    def handle_collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obtacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                        
        if direction == 'vertical':
            for sprite in self.obtacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
    
    def handle_movement(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed   
        self.handle_collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed   
        self.handle_collision('vertical')
        self.rect.center = self.hitbox.center
    
    def handle_angle(self):
        offset_x = pygame.mouse.get_pos()[0] - CENTER_X
        offset_y = pygame.mouse.get_pos()[1] - CENTER_Y
        if offset_y == 0:
            self.angle = math.pi / 2 if offset_x > 0 else -math.pi / 2
        else:
            self.angle = math.degrees(math.atan2(offset_y, offset_x))  
        self.image = pygame.transform.rotate(self.org_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.hitbox.center
    
    def display(self, surf, offset):
        offset_pos = self.hitbox.center - offset
        surf.blit(self.image, offset_pos)
    
    
    def handle_pygame_event(self, events : pygame.event.EventType):
        pass                
        
        
    def update(self):
        self.handle_angle()
        self.handle_key_input()
        self.handle_movement()
        
        
        
