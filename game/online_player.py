import pygame
import random, math
from game.player import Player
from game.settings import *
from game.ultis.resource_loader import get_sprite_from_sheet


class OnlinePlayer(Player):
    
    def __init__(self, spwan_pos, sprite_groups, obtacles_sprites, team="ct", id = ""):
        super().__init__(spwan_pos, sprite_groups, obtacles_sprites, team , id)
        self.speed = 5
        self.time = 0
        
    def handle_angle(self):
        self.image = pygame.transform.rotate(self.org_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.hitbox.center
        if self.selected_weapon:
            self.selected_weapon.rotate(-self.angle)
    
    def load_data(self, data):
        self.hitbox.center = data['pos']
        self.hp = data['hp']
        self.angle = data['angle']
        if self.selected_weapon_index != data['wp_index']:
            self.set_selected_weapon(self.weapons_list[data['wp_index']])
            self.selected_weapon_index = data['wp_index']
        if self.sprite_index != data['sp_index']:
            self.sprite_index = data['sp_index']
            self.org_image =  self.org_image = get_sprite_from_sheet(self.sprites_sheet, PLAYER_SIZE, self.sprite_index)
        
    def update(self):
        self.handle_angle()       
