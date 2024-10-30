import pygame, os
from game.bullet import Bullet, LineBullet
from game.ultis.resource_loader import import_csv_layout, get_tile_texture
from game.settings import *
from game.player import Player
from game.online_player import OnlinePlayer
from game.tile import Tile
from game.network import Network
from game.weapon import Gun, Knife
from game.input_event import InputEvent

class Map:
    def __init__(self):
        self.display_surface =  pygame.display.get_surface() 
        self.visible_sprites = CameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()
        self.online_player = pygame.sprite.Group()
        self.totals_player = pygame.sprite.Group()
        LineBullet.init_hit_obtacles(self.obstacles_sprites, self.totals_player)
        Gun.set_sprite_groups(self.visible_sprites)
        Knife.set_sprite_groups(self.visible_sprites)
        self.bullets = []
        self.bullets_data = []
        self.player_id = []
        self.network = Network()
        self.create_map()
        self.pygame_events = None
        self.events = InputEvent()
        # self.firing_sound = pygame.mixer.Sound('./assets/sounds/ak47.wav')
        
        
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('./assets/maps/dust2/dust2.csv',range(5,30))
        }
        for row_index, row in enumerate(layouts['boundary']):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val != -1:
                    Tile((x, y),[self.visible_sprites, self.obstacles_sprites], get_tile_texture('./assets/maps/dust2/dust2_tiles.png', val, TILE_SIZE))                    
        id = "tuyenlt"
        # id = input()
        self.local_player = Player((1300, 1200),[self.visible_sprites, self.totals_player], self.obstacles_sprites,"t", id)
        self.player_id.append(id)
        self.network.player_init(id)
        # self.local_player.set_selected_weapon(Gun(self.local_player, name="ak47"))
        self.visible_sprites.set_local_player(self.local_player)
        
                    
                    
    def update_pygame_events(self, events : list[pygame.event.EventType]):
        self.events.update_event(events)
                    
                     
    def event_handle(self):
        if self.events.mouse_clicking:
            if self.local_player.selected_weapon and self.local_player.selected_weapon.type == "auto":
                self.local_player.selected_weapon.fire(self.bullets, self.bullets_data)       
        def on_click():
            if self.local_player.selected_weapon and self.local_player.selected_weapon.type == "single": 
                self.local_player.selected_weapon.fire(self.bullets, self.bullets_data)
        self.events.on_click_callback = on_click
    
    def network_update(self):
        self.network.local_data = {
            'flag' : 2,
            'id' : self.local_player.id,
            'player' : {
                'pos' : self.local_player.hitbox.center,
                'hp' : self.local_player.hp,
                'angle' : self.local_player.angle,
                'online_bullets' : [],
                'local_bullets' : self.bullets_data,
                'weapon' : self.local_player.selected_weapon.name
            },
        }
        self.network.fetch_data()
        self.bullets_data.clear()
        
        for key in self.network.server_data['player'].keys():
            if key not in self.player_id and key != 'bullets':
                self.player_id.append(key)
                new_player = OnlinePlayer(self.network.server_data['player'][key]['pos'], [self.visible_sprites, self.totals_player], self.obstacles_sprites, "ct", key)
                new_player.set_selected_weapon(Gun(new_player ,self.network.server_data['player'][key]['weapon']))
                self.online_player.add(new_player)
                print(new_player.selected_weapon)
                
        for player in self.online_player:
            player.load_data(self.network.server_data['player'][player.id])
        
        for (start_pos, end_pos, angle, id) in self.network.server_data['player'][self.local_player.id]['online_bullets']:
            self.bullets.append(LineBullet(start_pos, angle, 
                                               id, 20, False))
            
        for player in self.totals_player:
            if player.hp <= 0:
                player.kill()
        
                     
    def run(self, mouse_clicking = False):
        self.event_handle()
        self.network_update()
        self.visible_sprites.update()
        self.visible_sprites.display(self.bullets, self.obstacles_sprites, self.totals_player)    
        
        
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
            if sprite.__class__.__name__ == 'Gun':
                pass
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        
        #* bullet hitting the player        
        for bullet in bullets:
            bullet.display(self.display_surface, self.offset)
            if bullet.display_frame == 0:
                bullets.remove(bullet)
                    