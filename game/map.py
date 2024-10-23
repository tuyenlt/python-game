import pygame, os
from game.bullet import Bullet
from game.ultis.resource_loader import import_csv_layout, get_tile_texture
from game.settings import *
from game.player import Player
from game.online_player import OnlinePlayer
from game.tile import Tile

class Map:
    def __init__(self):
        self.display_surface =  pygame.display.get_surface() 
        self.visible_sprites = CameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.bullets_sprites = pygame.sprite.Group()
        self.online_player = pygame.sprite.Group()
        self.create_map()
        self.events = None
        self.firing_sound = pygame.mixer.Sound('./assets/sounds/ak47.wav')
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./assets/maps/dust2.csv',2)
        }
        for row_index, row in enumerate(layouts['boundary']):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col != -1:
                    Tile((x, y),[self.visible_sprites, self.obstacles_sprites], get_tile_texture('./assets/maps/dust2.bmp',col,TILE_SIZE))                    
        self.local_player = Player((1300, 1200),[self.visible_sprites, self.online_player], self.obstacles_sprites,"ct", "tuyenlt")
        self.visible_sprites.set_local_player(self.local_player)
        self.online_player.add(OnlinePlayer((1000, 1700), [self.visible_sprites], self.obstacles_sprites, "t", "other1"))
        self.online_player.add(OnlinePlayer((1500, 1700), [self.visible_sprites], self.obstacles_sprites, "t", "other2"))
        self.online_player.add(OnlinePlayer((1100, 1200), [self.visible_sprites], self.obstacles_sprites, "t", "other3"))
        self.online_player.add(OnlinePlayer((1600, 1300), [self.visible_sprites], self.obstacles_sprites, "t", "other4"))
        self.online_player.add(OnlinePlayer((1500, 1300), [self.visible_sprites], self.obstacles_sprites, "t", "other5"))
        
                    
                    
    def update_events(self, events : list[pygame.event.EventType]):
        self.events = events
                    
                     
    def event_handle(self):
        for event in self.events:
            #* handle local player shooting bullet
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.firing_sound.play()
                Bullet(self.local_player.hitbox.center, self.local_player.angle, [self.bullets_sprites, self.visible_sprites],"tuyenlt")
                     
                     
    def run(self, mouse_clicking= False):
        if mouse_clicking and self.cooldown <= 0:
            self.bullets_sprites.append(Bullet(self.local_player.rect.center, self.local_player.angle, [self.visible_sprites]))
        self.event_handle()
        self.visible_sprites.display(self.bullets_sprites, self.obstacles_sprites, self.online_player)    
        self.visible_sprites.update()
        
        
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()       
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        self.floor_surf = pygame.image.load("./assets/maps/dust2.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        self.local_player = None
        
    def set_local_player(self, local_player):
        self.local_player = local_player    
        
    def display(self,bullets_sprites, obtacles_sprites, player_groups):
        #* get the offset
        self.offset.x = self.local_player.hitbox.centerx - CENTER_X
        self.offset.y = self.local_player.hitbox.centery - CENTER_Y
        #* draw floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos) 
        
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        
        #* bullet hitting the player        
        for bullet in bullets_sprites:
            for player in player_groups:
                if bullet.owner == player.id:
                    continue
                if bullet.hitbox.colliderect(player.hitbox):
                    print(f"player {player.id} was killed by {bullet.owner}")
                    player.kill()
                    bullet.kill()
                    