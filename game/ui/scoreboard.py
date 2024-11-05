import pygame

class Scoreboard:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/korean.ttf', 5)  
  
        
        self.tab_rect = pygame.Rect(0, 0, )
        self.tab_rect.center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)

        self.main_buttons = self.create_main_buttons()
        self.terrorists_buttons = self.create_terrorists_tab_buttons()
        self.counter_terrorists_buttons = self.create_counter_terrorists_tab_buttons()
        
        self.buttons = self.create_main_buttons()
        


    def draw_tab(self):        
            s = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
            s.set_alpha(0)  
            s.fill((190,158,108))
            self.display_surface.blit(s, (0, 0))
            
            tab_surface = pygame.Surface(self.tab_rect.size)
            tab_surface.fill((50, 50, 50)) 
            tab_surface.set_alpha(128)  
            self.display_surface.blit(tab_surface, self.tab_rect.topleft)
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.tab_rect, 2, border_radius=10)

            mouse_pos = pygame.mouse.get_pos()
            for name, rect in self.buttons.items():
                color = (100, 100, 100)  
                if rect.collidepoint(mouse_pos):
                    color = (150, 150, 150)

                pygame.draw.rect(self.display_surface, color, rect, border_radius=10)
                text_surf = self.font.render(name, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=rect.center)
                self.display_surface.blit(text_surf, text_rect)
