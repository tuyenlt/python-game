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
        pygame.display.set_caption("2D Shotting")
        self.clock = pygame.time.Clock()
        self.map = Map()
        self.events = NOEVENT
        
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
            self.screen.blit(self.map.pointer_image, self.map.pointer_rect)  # Vẽ cursor lên màn hình
            pygame.display.update()
            self.clock.tick(FPS)

        