import pygame
import math
from game.bullet import LineBullet
from game.settings import *
import random

# class Weapon(pygame.sprite.Sprite):
#     sprite_groups = None
#     def __init__(self, owner, name=""):
#         super().__init__(self.sprite_groups)
#         self.name = name
#         self.owner = owner
    


class Gun(pygame.sprite.Sprite):
    start_time = pygame.time.get_ticks()
    sprite_groups = None
    
    @classmethod
    def set_sprite_groups(cls, sprite_groups): #! call this func before create any object
        cls.sprite_groups = sprite_groups
    
    def __init__(self, owner , name = "ak47"):
        super().__init__(self.sprite_groups)
        self.name = name
        self.owner = owner
        self.gun_attr_init()
        
        self.fire_sound = pygame.mixer.Sound(f"./assets/sounds/weapons/{self.name}.wav")
        self.fire_sound.set_volume(10)
        self.org_image = pygame.image.load(f"./assets/gfx/weapons/{self.name}.bmp").convert_alpha()
        self.reload_start_sound = pygame.mixer.Sound("./assets/sounds/weapons/reloadstart.wav")
        self.reload_end_sound = pygame.mixer.Sound("./assets/sounds/weapons/reloadend.wav")
        
        self.image = self.org_image
        self.rect = self.image.get_rect()
        self.offset_x = math.cos(10 * (2 * math.pi / 360)) * 20
        self.offset_y = math.sin(10 * (2 * math.pi / 360)) * 20
        self.angle = 0
        self.fire_cooldown = self.fire_rate
        self.reload_time_cnt = self.reload_time
        self.recoil_cnt = 0
    
    def gun_attr_init(self):
        if self.name == "ak47":            
            self.type = "auto"
            self.fire_rate = 0.12
            self.recoil = 6
            self.max_bullets = 30
            self.reload_time = 3
            self.dmg = 25
            self.recoil_increase = 1
            
        elif self.name == "m4a1":
            self.type = "auto"
            self.fire_rate = 0.11
            self.recoil = 4
            self.max_bullets = 30
            self.reload_time = 3
            self.dmg = 24
            self.recoil_increase = 0.8
            
        elif self.name == "glock18":
            self.type = "single"
            self.fire_rate = 0.1
            self.recoil = 0
            self.max_bullets = 21
            self.reload_time = 3
            self.dmg = 11
            self.recoil_increase = 1
            
        elif self.name == "usp":
            self.type = "single"
            self.fire_rate = 0.1
            self.recoil = 0
            self.max_bullets = 12
            self.reload_time = 3
            self.dmg = 15
            self.recoil_increase = 1
        else :
            self.type = "auto"
            self.fire_rate = 0.1
            self.recoil = 5
            self.max_bullets = 30
            self.reload_time = 1
            self.dmg = 10
        self.bullets_remain = self.max_bullets
    
    def rotate(self, angle):
        self.angle = -angle
        self.offset_x = math.cos(self.angle * (2 * math.pi / 360)) * 32
        self.offset_y = math.sin(self.angle * (2 * math.pi / 360)) * 32
        self.image = pygame.transform.rotate(self.org_image, angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.owner.hitbox.centerx + self.offset_x
        self.rect.centery = self.owner.hitbox.centery + self.offset_y 
        
    def fire(self, bullets_list = [], bullets_data = []):
        if self.bullets_remain == 0:
            return
        if self.type == "auto":
            if self.fire_cooldown > 0:
                return
            if self.fire_cooldown > -self.fire_rate:
                if int(self.recoil_cnt) != 0:
                    recoil = random.randrange(int(-self.recoil_cnt), int(self.recoil_cnt))
                else:
                    recoil = 0
                if self.recoil_cnt < self.recoil:
                    self.recoil_cnt += self.recoil_increase
            else:
                recoil = 0
                self.recoil_cnt = 0
        elif self.type == "single":
            recoil = 0
            
        self.fire_cooldown = self.fire_rate
        self.fire_sound.stop()
        self.fire_sound.play()
        self.bullets_remain -= 1
        new_bullet = LineBullet(self.owner.hitbox.center, self.angle + recoil, self.owner.id, self.dmg)
        bullets_list.append(new_bullet)
        bullets_data.append(new_bullet.to_object_value())
    
    
            
    def update(self):
        self.fire_cooldown -= 1 / FPS
        if self.bullets_remain == 0:
            if self.reload_time_cnt == self.reload_time:
                self.reload_start_sound.play()
            if abs(int(self.reload_time_cnt * 100) - 150) <= 100 / FPS:
                self.reload_end_sound.play()
            self.reload_time_cnt -= 1 / FPS
        if self.reload_time_cnt <= 0:
            self.reload_time_cnt = self.reload_time
            self.bullets_remain = self.max_bullets
            


class Knife(pygame.sprite.Sprite):
    sprite_groups = None
    
    @classmethod
    def set_sprite_groups(cls, sprite_groups): #! call this func before create any object
        cls.sprite_groups = sprite_groups
    
    def __init__(self, owner):
        super().__init__(self.sprite_groups)
        self.name = "knife"
        self.type = "auto"
        self.owner = owner
        self.slash_sound = pygame.mixer.Sound(f"./assets/sounds/weapons/{self.name}_hit.wav")
        self.org_image = pygame.image.load(f"./assets/gfx/weapons/{self.name}.bmp").convert_alpha()
        self.image = self.org_image
        self.rect = self.image.get_rect()
        self.offset_x = math.cos(10 * (2 * math.pi / 360)) * 20
        self.offset_y = math.sin(10 * (2 * math.pi / 360)) * 20
        self.angle = 0
        self.slash_cooldown = 0
        self.slash_delay = 0.4
    
    def fire(self, x, y):
        if self.slash_cooldown > 0:
            return
        self.slash_cooldown = 0.4
        self.slash_sound.play()
        self.owner.onslash = True
        self.owner.knife_slash_animation()
        print("xien chet cu may di")
    
    def rotate(self, angle):
        self.angle = -angle
        self.offset_x = math.cos(self.angle * (2 * math.pi / 360)) * 32
        self.offset_y = math.sin(self.angle * (2 * math.pi / 360)) * 32
        self.image = pygame.transform.rotate(self.org_image, angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.owner.hitbox.centerx + self.offset_x
        self.rect.centery = self.owner.hitbox.centery + self.offset_y     
        
    def update(self, *args, **kwargs):
        self.slash_cooldown -= 1 / FPS
        
        