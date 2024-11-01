import pygame, sys
from pygame.locals import *
from game.settings import *
from game.map import Map
from game.ui.button import Button


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SRC_WIDTH, SRC_HEIGHT))
        pygame.display.set_caption("2D Shootting")
        self.clock = pygame.time.Clock()
        self.map = Map()
        self.events = NOEVENT
        
        self.font = pygame.font.Font('assets/fonts/digital-7.ttf', 30)
        
    def run(self):
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.map.network.shut_down()
                    sys.exit()
            self.screen.fill((255, 255, 255))
            self.map.update_pygame_events(self.events)    
            self.map.run()
            
            #draw pointer
            self.map.pointer_rect.center = pygame.mouse.get_pos()
            self.screen.blit(self.map.pointer_image, self.map.pointer_rect)
            
            fps = self.clock.get_fps()
            interger_part = int(fps)
            decimal_part = fps - interger_part
            
            if decimal_part >= 0.5 :
                fps = interger_part + 1
            else :
                fps = interger_part
            fps_text_render = self.font.render(f'FPS : {str(int(fps))}', False, (255,232,80))
            fps_text_rect = fps_text_render.get_rect()
            x = 20  
            y = 20
            fps_text_rect.topleft = x, y
            
            self.screen.blit(fps_text_render, fps_text_rect)
            
            pygame.display.update()
            self.clock.tick(FPS)