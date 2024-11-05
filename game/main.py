import pygame, sys, time
from pygame.locals import *
from game.settings import *
from game.gameclient import GameClient
from game.ui.button import Button
from game.ui.menu import Menu
from game.network import Network
from game.introduction.intro import Intro
from game.introduction.start_menu import StartMenu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SRC_WIDTH, SRC_HEIGHT))
        pygame.display.set_caption("2D Shootting")
        self.clock = pygame.time.Clock()
        self.game_client = None
        self.events = NOEVENT
        
        self.font = pygame.font.Font('assets/fonts/digital-7.ttf', 30)
        self.menu = Menu()
        self.network = Network()  
        
        
    
    def main_menu(self):
        running  = True
        self.start_menu = StartMenu()
        while(running) :
        # print("active server")
        # print(self.network.get_servers_list())
        # # name  = input()
        # name  = "dfsds"
        # (address) = self.network.create_new_server(name)
        # print(address)
        # (host, port) = address
        # self.network.join_server(host, port)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == KEYDOWN and event.key == pygame.K_RETURN and self.start_menu.change_name:
                    self.start_menu.default_name = self.start_menu.name_input.text
                    self.start_menu.change_name = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for name, rect in self.start_menu.buttons:
                        if rect.collidepoint(mouse_pos):
                            if name == 'Create' :
                                (host, port) = self.network.create_new_server("tuyenlt")
                                self.start_menu.addr = (host, port)
                                running = False
                            elif name == 'Join' :
                                self.start_menu.init_join_buttons(self.network.get_servers_list())
                                self.start_menu.join = True
                                self.start_menu.change_name = False  
                                                     
                            elif name == 'Change Name' :
                                self.start_menu.change_name = True
                                self.start_menu.join = False
                                self.start_menu.draw_change_name()
                            elif name == 'Quit' :
                                pygame.QUIT
                                sys.exit()
                                
                    if self.start_menu.join:
                        for name, rect,host, port in self.start_menu.join_buttons:
                            if rect.collidepoint(mouse_pos):
                                self.start_menu.addr = (host, port)
                                running = False
                if self.start_menu.change_name:
                    self.start_menu.name_input.handle_event(event)                
            self.start_menu.draw()
            pygame.display.update()
            self.clock.tick(FPS)  
        
    def run_intro(self):
        running = True
        self.intro = Intro()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    running = False
                        
            pygame.display.update()
            self.clock.tick(FPS)  
            self.intro.draw()
        

    def run(self):
        self.run_intro()
        print(self.network.get_servers_list())
        self.main_menu()
        (host, port) = self.start_menu.addr
        self.network.join_server(host, port)
        while True:
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    if self.game_client:
                        self.game_client.network.shut_down(self.game_client.local_player.id)
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:  
                    self.menu.toggle()
                    self.menu.buttons = self.menu.main_buttons
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  
                    self.game_client = None
                self.menu.handle_event(event)
            
            if self.menu.val not in ["", "t", "ct"]:
                if not self.game_client:
                    self.game_client = GameClient(self.start_menu.default_name, self.menu.val, self.network)
                else:
                    self.network.change_team_request(self.game_client.local_player.id, self.menu.val)    
                    self.game_client.local_player.switch_team(self.menu.val)
                self.menu.val = ""
                    
            if self.game_client:
                self.screen.fill((255,255,255))
                self.game_client.event_handle(self.events)    
                self.game_client.run()
                self.game_client.pointer_rect.center = pygame.mouse.get_pos()
                self.screen.blit(self.game_client.pointer_image, self.game_client.pointer_rect)
            else:
                self.screen.fill((190,158,108))
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