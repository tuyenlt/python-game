import pygame
import time

class UI:
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/digital-7.ttf', 60)
        
        # Countdown timer initialization
        self.start_time = time.time()
        self.countdown_seconds = 5 * 60  # 5 minutes in seconds

    def show_hp(self, hp):
        # hp_text_surf
        hp_text_render = self.font.render(str(int(hp)), False, (255,232,80))
        hp_text_rect = hp_text_render.get_rect()

        #hp_symbol
        hp_symbol_surf = pygame.transform.scale(pygame.image.load('assets/fonts/health.webp'), (55,55))
        hp_symbol_rect = hp_symbol_surf.get_rect()
        
        #hp_symbol_pos
        x = 20  
        y = self.display_surface.get_size()[1] - 20 
        hp_symbol_rect.bottomleft = (x, y)
        
        hp_text_rect.center = hp_symbol_rect.centerx + hp_symbol_rect.width + 20, hp_symbol_rect.centery
        
        
        self.display_surface.blit(hp_text_render, hp_text_rect)
        self.display_surface.blit(hp_symbol_surf, hp_symbol_rect)

    def show_timer(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = self.countdown_seconds - elapsed_time
        
        if remaining_time < 0:
            remaining_time = 0  

        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)

        timer_text = f"{minutes:02}:{seconds:02}"  
        timer_text_render = self.font.render(timer_text, False, (255,232,80))  
        timer_rect = timer_text_render.get_rect()
        
        timer_symbol = pygame.transform.scale(pygame.image.load('assets/fonts/clock.png').convert_alpha(), (55, 55))
        timer_symbol_rect = timer_symbol.get_rect()

        
        x = self.display_surface.get_size()[0] // 2
        y = self.display_surface.get_size()[1] - 20 - timer_text_render.get_height()

        timer_rect.centerx = x  
        timer_rect.y = y

        
        timer_symbol_rect.midright = (timer_rect.midleft[0] - 20, timer_rect.midleft[1])

        
        self.display_surface.blit(timer_text_render, timer_rect)
        self.display_surface.blit(timer_symbol, timer_symbol_rect)

    def show_bullet(self, bullet_remain):
        # hp_text_surf
        hp_text_render = self.font.render(str(int('abc')), False, (255,232,80))
        hp_text_rect = hp_text_render.get_rect()

        #hp_symbol
        hp_symbol_surf = pygame.transform.scale(pygame.image.load('assets/fonts/3401408.webp'), (55,55))
        hp_symbol_rect = hp_symbol_surf.get_rect()
        
        #hp_symbol_pos
        x = 20  
        y = self.display_surface.get_size()[1] - 20 
        hp_symbol_rect.bottomleft = (x, y)
        
        hp_text_rect.center = hp_symbol_rect.centerx + hp_symbol_rect.width + 20, hp_symbol_rect.centery
        
        
        self.display_surface.blit(hp_text_render, hp_text_rect)
        self.display_surface.blit(hp_symbol_surf, hp_symbol_rect)

    def display(self, player):
        self.show_hp(player.hp)
        self.show_timer()  
