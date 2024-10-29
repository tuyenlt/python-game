import pygame
from game.settings import *
import math
from game.ultis.func import *
from game.tile import Tile

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

class LineBullet():
    RANGE_BUFFER = 10000
    def __init__(self,start_pos,angle, owner, obtacles, players):
        self.angle = angle
        (x, y) = start_pos
        x += math.cos(self.angle * (2 * math.pi / 360)) * 40
        y += math.sin(self.angle * (2 * math.pi / 360)) * 40
        self.start_pos = (x, y)
        self.end_x = start_pos[0] + math.cos(self.angle * (2 * math.pi / 360)) * self.RANGE_BUFFER
        self.end_y = start_pos[1] + math.sin(self.angle * (2 * math.pi / 360)) * self.RANGE_BUFFER
        self.owner = owner
        self.caculate_hit_pos(obtacles, players)
        self.color = (255,255,0)
        self.display_frame = 5
    
    def to_object_value(self):
        return (self.start_pos, (self.end_x, self.end_y), self.angle, self.owner)
    
    def caculate_hit_pos(self, obtacles, players):
        possible_hit_pos = []
        for obtacle in obtacles:
            obtacle_x, obtacle_y = obtacle.rect.topleft
            hit_pos = liang_barsky((obtacle_x, obtacle_y, obtacle_x + TILE_SIZE, obtacle_y + TILE_SIZE), self.start_pos, (self.end_x, self.end_y))
            if hit_pos != None:
                possible_hit_pos.append(hit_pos)
                
        for player in players:
            player_x, player_y = player.hitbox.topleft
            hit_pos = liang_barsky((player_x, player_y, player_x + PLAYER_SIZE, player_y + PLAYER_SIZE), self.start_pos, (self.end_x, self.end_y))
            if hit_pos != None:
                possible_hit_pos.append(hit_pos)
        
        possible_hit_pos.sort(key = lambda pos : distance(pos, self.start_pos))
        self.hit_x , self.hit_y = possible_hit_pos[0] if possible_hit_pos.__len__() > 0 else (self.end_x, self.end_y)
    
    def display(self, surf, offset):
        dx = math.cos(self.angle * (2 * math.pi / 360)) * 10
        dy = math.sin(self.angle * (2 * math.pi / 360)) * 10
        self.start_pos = (self.start_pos[0] + dx, self.start_pos[1] + dy)
        start_pos = self.start_pos - offset
        end_pos = (self.hit_x, self.hit_y) - offset
        pygame.draw.line(surf, self.color, start_pos, end_pos, 1)
        self.display_frame -= 1
        