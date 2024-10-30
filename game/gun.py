import pygame
import math
from game.bullet import LineBullet
from game.settings import *
import random

class Gun(pygame.sprite.Sprite):
    start_time = pygame.time.get_ticks()
    def __init__(self, groups, owner , name = "ak47"):
        super().__init__(groups)
        self.name = name
        self.owner = owner
        self.gun_attr_init()
        self.fire_sound = pygame.mixer.Sound(f"./assets/sounds/weapons/{self.name}.wav")
        self.fire_sound.set_volume(30)
        self.org_image = pygame.image.load(f"./assets/gfx/weapons/{self.name}.bmp").convert_alpha()
        self.reload_start_sound = pygame.mixer.Sound("./assets/sounds/weapons/reloadstart.wav")
        self.reload_end_sound = pygame.mixer.Sound("./assets/sounds/weapons/reloadend.wav")
        self.image = self.org_image
        self.rect = self.image.get_rect()
        self.offset_x = math.cos(10 * (2 * math.pi / 360)) * 20
        self.offset_y = math.sin(10 * (2 * math.pi / 360)) * 20
        self.gun_attr_init()
        self.angle = 0
        self.fire_cooldown = self.fire_rate
        self.reload_time_cnt = self.reload_time
        self.recoil_cnt = 0
    
    def gun_attr_init(self):
        if self.name == "ak47":            
            self.type = "auto"
            self.fire_rate = 0.1
            self.recoil = 6
            self.max_bullets = 30
            self.reload_time = 3
            self.dmg = 20
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
        if self.fire_cooldown > 0 or self.bullets_remain == 0:
            return
        if self.fire_cooldown > -self.fire_rate:
            if self.recoil_cnt != 0:
                recoil = random.randrange(-self.recoil_cnt, self.recoil_cnt)
            else:
                recoil = 0
            if self.recoil_cnt < self.recoil:
                self.recoil_cnt += self.recoil_increase
        else:
            recoil = 0
            self.recoil_cnt = 0
            
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
        pass