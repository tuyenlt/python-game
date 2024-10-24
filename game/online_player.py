import pygame
import random, math
from game.player import Player


class OnlinePlayer(Player):
    
    def __init__(self, spwan_pos, sprite_groups, obtacles_sprites, team="ct", id = ""):
        super().__init__(spwan_pos, sprite_groups, obtacles_sprites, team , id)
        self.speed = 5
        self.time = 0
    
    def handle_angle(self):
        self.angle = random.randint(0,360)
        self.image = pygame.transform.rotate(self.org_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.hitbox.center
    
    def update(self):
        # update from the server
        self.handle_movement()
        self.time += 1
        if self.time % 100 == 0:
            self.direction.x = (random.randint(0,10) - 5) / 10 
            self.direction.y = (random.randint(0,10) - 5) / 10
        if self.time % 20 == 0:
            self.handle_angle()
        pass    