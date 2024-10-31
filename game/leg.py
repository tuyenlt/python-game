import pygame
from game.ultis.resource_loader import *
class Leg(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        # animations
        self.moves = get_animation_from_img('assets/player/legs.bmp', 32, (255, 0, 255))
        self.frame_index = 0
        self.animation_speed = 0.15
        
        
        keys = pygame.key.get_pressed()
       
        animation = []
        for index in range(len(self.moves)) :
            if index >= 2 :
                animation.append(self.moves[index])
        
        #loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation) :
            self.frame_index = 0
        #set the image
        self.image = pygame.transform.rotate(animation[int(self.frame_index)], player.angle)
        self.rect = self.image.get_rect(center = player.hitbox.center)