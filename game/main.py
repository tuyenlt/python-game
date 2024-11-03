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
            if self.map:
                self.screen.fill((255,255,255))
                self.map.event_handle(self.events)    
                self.map.run()
            else:
                self.screen.fill((190,158,108))
            
            #draw pointer
            if self.map:
                self.map.pointer_rect.center = pygame.mouse.get_pos()
                self.screen.blit(self.map.pointer_image, self.map.pointer_rect)
            
            self.menu.draw()
            
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
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.active:
            mouse_pos = pygame.mouse.get_pos()
            for name, rect in self.menu.buttons.items():
                if rect.collidepoint(mouse_pos):
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        print(f"{name} button clicked")
                        if name == 'Terrorists' :
                            self.menu.toggle()
                            if event.type == pygame.MOUSEBUTTONDOWN and self.menu.sub_menu_active:
                                for sub_name, sub_rect in self.menu.sub_buttons.items():
                                    if sub_rect.collidepoint(mouse_pos):
                                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                            print(f"{sub_name} button clicked")
                                            self.menu.toggle()
                            if not self.map:
                                self.map = Map('toan', "t")
                            else:
                                self.map.local_player.switch_team("t")
                                self.map.network.change_team_request(self.map.local_player.id,"t")
                        elif name == 'Counter-Terrorists' :
                            if not self.map:
                                self.map = Map('tuyen', "ct")
                            else:
                                self.map.local_player.switch_team("ct")
                                self.map.network.change_team_request(self.map.local_player.id,"ct")
                        else :
                            self.menu.toggle()
                            