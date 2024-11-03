import pygame
import math
import os
import json
from game.settings import *
from game.ultis.resource_loader import *
from game.weapon import Gun, Knife, Grenade
from game.ultis.func import TimerCallback


class Player(pygame.sprite.Sprite):
    
    def __init__(self, spawn_pos, sprite_groups, obtacles_sprites, team, id = "tuyenlt"):
        super().__init__(sprite_groups)
        self.sprite_groups = sprite_groups[0]
        #* display init
        self.sprites_sheet = pygame.image.load(f"./assets/gfx/player/{team}1.bmp").convert_alpha()
        self.org_image = get_tile_texture(f'./assets/gfx/player/{team}1.bmp', 0, 64)
        self.dead_image = pygame.image.load(f"./assets/gfx/player/dead.png")
        
        self.image = self.org_image
        self.obtacles_sprites = obtacles_sprites
        self.sprite_index = 0
        self.rect = self.image.get_rect(topleft = spawn_pos)
        self.hitbox = self.rect
        self.team = team
        self.id = id
        self.hp = 100
        
        
        #* attr init
        self.angle = 0
        self.direction = pygame.math.Vector2()
        self.speed = 5
        
        #*init for knife slash
        self.delta_slash_angle = 6
        self.onslash = False
        self.slash_time = 0.4
        self.slash_time_cnt = 0.4
        
        self.dead = False
        self.firing = False
        self.respawn_pos = spawn_pos
        self.respawn_call_back = None
        self.respawn_hook = TimerCallback(2, self.respawn)
        self.bullets = []
        self.knife_sl = []
        self.explode_nade = []
        self.sound_channel = None

        
    def weapons_init(self):
        self.weapons_list = [None] * 6
        if self.team == 'ct':
            self.weapons_list[1] = Gun( owner=self, sound_channel= self.sound_channel ,name="m4a1")
            self.weapons_list[2] = Gun( owner=self, sound_channel= self.sound_channel ,name="usp")
        if self.team == 't':
            self.weapons_list[1] = Gun( owner=self, sound_channel= self.sound_channel ,name="ak47")
            self.weapons_list[2] = Gun( owner=self, sound_channel= self.sound_channel ,name="glock18")
        self.weapons_list[3] = Knife( owner= self, sound_channel= self.sound_channel)
        self.weapons_list[4] = Grenade( owner= self,sound_channel= self.sound_channel,name="he")
        Gun.sprite_groups.remove(self.weapons_list[2])
        Gun.sprite_groups.remove(self.weapons_list[3])
        Gun.sprite_groups.remove(self.weapons_list[4])
        self.selected_weapon = self.weapons_list[1]
        self.selected_weapon_index = 1
        
    def sound_channel_init(self, sound_channel):
        self.sound_channel = sound_channel
    
    def set_volume(self, volume):
        self.sound_channel.set_volume(volume)
    
    def set_selected_weapon(self, weapon):
        if weapon != self.selected_weapon:
            Gun.sprite_groups.remove(self.selected_weapon)
            Gun.sprite_groups.add(weapon)
            self.selected_weapon = weapon
        
    
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
        
        if keys[pygame.K_LCTRL]:
            self.speed = 2.5
        else:
            self.speed = 5
        #********** end movement input

        #********** weapon input
        if keys[pygame.K_1]:
            self.set_selected_weapon(self.weapons_list[1])
            self.org_image = get_sprite_from_sheet(self.sprites_sheet, PLAYER_SIZE, 0)
            self.selected_weapon_index = 1
            self.sprite_index = 0
            
        if keys[pygame.K_2]:
            self.set_selected_weapon(self.weapons_list[2])
            self.org_image = get_sprite_from_sheet(self.sprites_sheet, PLAYER_SIZE, 4)
            self.selected_weapon_index = 2
            self.sprite_index = 4
            
        if keys[pygame.K_3]:
            self.set_selected_weapon(self.weapons_list[3])
            self.org_image = get_sprite_from_sheet(self.sprites_sheet, PLAYER_SIZE, 2)
            self.selected_weapon_index = 3
            self.sprite_index = 2
            
        if keys[pygame.K_4]:
            if self.weapons_list[4].bullets_remain > 0:
                self.set_selected_weapon(self.weapons_list[4])
                self.org_image = get_sprite_from_sheet(self.sprites_sheet, PLAYER_SIZE, 2)
                self.selected_weapon_index = 4
                self.sprite_index = 2
            
        if keys[pygame.K_r]:
            if self.selected_weapon_index in [1,2]:
                self.selected_weapon.reload()
        
    def switch_to_primary_weapon(self):
        self.set_selected_weapon(self.weapons_list[1])
        self.org_image = get_sprite_from_sheet(self.sprites_sheet, PLAYER_SIZE, 0)
        self.selected_weapon_index = 1
        self.sprite_index = 0
    
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
        if not self.onslash:
            offset_x = pygame.mouse.get_pos()[0] - CENTER_X
            offset_y = pygame.mouse.get_pos()[1] - CENTER_Y
            if offset_y == 0:
                self.angle = -180 if offset_x < 0 else 0
            else:
                self.angle = math.degrees(math.atan2(offset_y, offset_x))  
        self.image = pygame.transform.rotate(self.org_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.hitbox.center
        if self.selected_weapon:
            self.selected_weapon.rotate(-self.angle)
        
    
    def display(self, surf, offset):
        offset_pos = self.hitbox.center - offset    
        surf.blit(self.image, offset_pos)    
    
    def knife_slash_animation(self): 
        if self.slash_time_cnt >= self.slash_time / 2:
            self.angle += self.delta_slash_angle
        elif 0 <= self.slash_time_cnt <= self.slash_time / 2:
            self.angle -= self.delta_slash_angle
        else :
            self.slash_time_cnt = self.slash_time
            self.onslash = False
        self.slash_time_cnt -= 1/FPS
    
    def load_data(self, data):
        self.hp = data['hp']
        if self.dead == False:
            self.dead = data['dead']
    
    def fire(self):
        if self.selected_weapon:
            self.selected_weapon.fire()
    
    def respawn(self):
        print("respawn call")
        self.rect.topleft = self.respawn_pos
        self.hitbox.center = self.rect.center
        self.hp = 100
        self.dead = False
        self.respawn_call_back()
        self.org_image = get_sprite_from_sheet(self.sprites_sheet, PLAYER_SIZE, 0)
        self.sprite_index = 0
        Gun.sprite_groups.add(self.selected_weapon)
        for weapon in self.weapons_list:
            if weapon != None:
                weapon.reset()
        
    def update(self):
        if self.onslash:
            self.knife_slash_animation()
        if self.dead:
            if self.respawn_hook.time_cnt == self.respawn_hook.delay_time:
                print("pass")
                self.org_image = self.dead_image
                self.image = self.org_image
                self.rect = self.image.get_rect()
                self.rect.center = self.hitbox.center
                Gun.sprite_groups.remove(self.selected_weapon)
                self.sprite_index = -1
                
            self.respawn_hook.count_down(1/FPS)
        else:
            self.handle_key_input()
            self.handle_movement()
            self.handle_angle()

    def get_data(self):
        data = {
            'team' : self.team,
            'pos' : self.hitbox.center,
            'hp' : self.hp,
            'angle' : self.angle,
            'wp_index' : self.selected_weapon_index,
            'sp_index' : self.sprite_index,
            'bullets' : self.bullets,
            'knife_sl': self.knife_sl,
            'nade': self.explode_nade,
            'firing': self.firing
        }
        return data
        
    def kill(self):
        for weapon in self.weapons_list:
            if weapon != None:
                weapon.kill()
        super().kill()        
    
        
