import pygame, random
from functools import partial
from game.bullet import Bullet, LineBullet
from game.ultis.resource_loader import import_csv_layout, get_tile_texture, get_animation_from_img
from game.settings import *
from game.player import Player
from game.online_player import OnlinePlayer
from game.tile import Tile
from game.network import Network
from game.weapon import Gun, Knife, Weapon
from game.input_event import InputEvent
from game.leg import Leg
from game.ultis.func import distance
from game.ui.message_bar import MessageBar

from game.ui.ui import UI
class Map:
    def __init__(self, id, team):
        self.display_surface =  pygame.display.get_surface() 
        self.visible_sprites = CameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.online_player = pygame.sprite.Group()
        self.totals_player = pygame.sprite.Group()
        self.player_id = []
        self.bullets = []
        self.network = Network()
        self.mouse_clicking = False
        self.sound_channel_cnt = 0
        self.msg_bar = MessageBar((SRC_WIDTH - 400, 100), (400, SRC_HEIGHT - 200), 80)
        
        LineBullet.init_hit_obtacles(self.obstacles_sprites, self.totals_player)
        Weapon.init(self.visible_sprites, self.obstacles_sprites)
        self.create_map(id, team)
        Gun.init(self.bullets)
        
        # self.select_team = None
        
        
        self.pygame_events = None
        # self.firing_sound = pygame.mixer.Sound('./assets/sounds/ak47.wav')
        
        
        
        #pointer 
        self.pointer_image = get_animation_from_img('assets/images/pointer.bmp', 46, (255, 0, 255))[0]
        self.pointer_rect = self.pointer_image.get_rect()
        
        # UI
        self.ui = UI()
        
    def set_team(self, team):
        self.select_team = team
        
    def create_map(self, id, team):
        layouts = {
            'boundary': import_csv_layout('./assets/maps/dust2/dust2.csv',range(5,30)),
            'spawn' : import_csv_layout('./assets/maps/dust2/dust2.csv', [47, 48])
        }
        for row_index, row in enumerate(layouts['boundary']):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val != -1:
                    Tile((x, y),[self.visible_sprites, self.obstacles_sprites])                    
           
        (spawn_x, spawn_y) = self.network.player_init(id, team)
        self.local_player = Player((spawn_x, spawn_y),[self.visible_sprites, self.totals_player], self.obstacles_sprites, team, id)
        self.local_player.sound_channel_init(pygame.mixer.Channel(self.sound_channel_cnt))
        self.local_player.set_volume(30)
        self.local_player.weapons_init()
        self.sound_channel_cnt += 1
        self.player_id.append(id)
        self.visible_sprites.set_local_player(self.local_player)
                     
    def event_handle(self, events : list[pygame.event.EventType]):
        for event in events:
            if event.type ==  pygame.MOUSEBUTTONDOWN:                
                if event.button == 1:
                    if self.local_player.selected_weapon.type == "single":
                        self.local_player.firing = True
                    self.mouse_clicking = True
            if event.type ==  pygame.MOUSEBUTTONUP:                
                if event.button == 1:
                    self.mouse_clicking = False
                    
        if self.local_player.selected_weapon.type == "auto":
            self.local_player.firing = self.mouse_clicking
        if self.local_player.firing:
            self.local_player.fire()

    def volume_control(self):
        for player in self.online_player:
            location_diff = distance(self.local_player.hitbox.center, player.hitbox.center)
            if location_diff > 2000:
                player.set_volume(0)
                continue
            player.set_volume(1 - (location_diff / 2000))
            
    
    def network_update(self):
        self.network.local_data = {
            'flag' : 2,
            'id' : self.local_player.id,
            'player' : self.local_player.get_data()
        }
        # print(self.local_player.firing)
        self.network.fetch_data()
        self.local_player.bullets.clear()
        self.local_player.knife_sl.clear()
        self.local_player.explode_nade.clear()
        self.local_player.firing = False
        
        for key in self.network.server_data['player'].keys():
            if key not in self.player_id and key != 'bullets':
                self.player_id.append(key)
                new_player = OnlinePlayer(self.network.server_data['player'][key]['pos'], [self.visible_sprites, self.totals_player],
                                             self.obstacles_sprites, self.network.server_data['player'][key]['team'] , key)
                new_player.sound_channel_init(pygame.mixer.Channel(self.sound_channel_cnt))
                new_player.weapons_init()
                self.sound_channel_cnt += 1
                self.online_player.add(new_player)
                
        for player in self.totals_player:
            if player.id not in self.network.server_data['player'].keys():
                player.kill()
                continue
            player.load_data(self.network.server_data['player'][player.id])
        
        for player in self.online_player:
            if player.firing == True:
                print("boom boom")
                player.fire()
        self.msg_bar.update(self.network.server_data['msg'])                
                     
    def run(self, mouse_clicking = False):
        self.volume_control()
        self.visible_sprites.update()
        self.network_update()
        self.visible_sprites.display(self.bullets, self.obstacles_sprites, self.totals_player)    
        self.ui.display(self.local_player)
        self.msg_bar.display()
                
        
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()       
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        
        self.floor_surf = pygame.image.load("./assets/maps/dust2/dust2.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        self.local_player = None
        
    def set_local_player(self, local_player):
        self.local_player = local_player    
        
    def display(self,bullets, obtacles_sprites, player_groups):
        #* get the offset
        self.offset.x = self.local_player.hitbox.centerx - CENTER_X
        self.offset.y = self.local_player.hitbox.centery - CENTER_Y
        #* draw floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos) 
        
        for sprite in self.sprites():
            if sprite.__class__.__name__ == 'Tile':
                continue
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        
        #* bullet hitting the player        
        for bullet in bullets:
            bullet.display(self.display_surface, self.offset)
            if bullet.display_frame == 0:
                bullets.remove(bullet)
                    