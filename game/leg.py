import pygame
from game.ultis.resource_loader import *
class Leg(pygame.sprite.Sprite):
    sprite_group = None
    
    # def init(cls, sprite_group):
    #     cls.sprite_group = sprite_group
    
    def __init__(self, player, groups):
        super().__init__(groups)
        # animations
        self.moves = get_animation_from_img('assets/player/legs.bmp', 32, (255, 0, 255))
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.moves[0]
        self.rect = self.image.get_rect(center=player.rect.center)
        
    def animate(self, player):
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.moves) :
            self.frame_index = 0
        #set the image
        self.image = pygame.transform.scale(self.moves[int(self.frame_index)], (100, 100))
        self.rect.center = player.rect.center
    
    def update_leg(self, player):
        self.animate(player)
    