import pygame, sys
from pygame.locals import *
from game.settings import *
from game.map import Map
from game.ui.button import Button
from game.ui.menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SRC_WIDTH, SRC_HEIGHT))
        pygame.display.set_caption("2D Shootting")
        self.clock = pygame.time.Clock()
        self.map = None
        self.events = NOEVENT
        
        self.font = pygame.font.Font('assets/fonts/digital-7.ttf', 30)
        self.menu = Menu()
        
    def run(self):
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    if self.map:
                        self.map.network.shut_down()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.menu.toggle()
                self.handle_event(event)
                    
                
            if not self.map:
                self.screen.fill((190,158,108))
            else :
                self.screen.fill((255,255,255))
            
            self.menu.draw()
            
            if self.map:
                self.map.update_pygame_events(self.events)    
                self.map.run()
            
            #draw pointer
            if self.map:
                self.map.pointer_rect.center = pygame.mouse.get_pos()
                self.screen.blit(self.map.pointer_image, self.map.pointer_rect)
            
            
            #show fps
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
    
    #menu handle event
    def handle_event(self, event):
        if self.menu.active:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for name, rect in self.menu.buttons.items():
                    if rect.collidepoint(mouse_pos):
                            print(f"{name} button clicked")
                            if name == 'Terrorists' :
                                # self.menu.toggle()
                                
                                self.map = Map('toan', "t")
                            elif name == 'Counter-Terrorists' :
                                self.map = Map('tuyen', "ct")
                            else :
                                self.menu.toggle()
            elif self.menu.sub_menu_active:
                for sub_name, sub_rect in self.menu.sub_buttons.items():
                    if sub_rect.collidepoint(mouse_pos):
                        self.menu.toggle()
                        print(f"{sub_name} button clicked")

