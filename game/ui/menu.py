import pygame

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/korean.ttf', 20)  
        self.active = True  
        self.sub_menu_active = False
        
        self.menu_rect = pygame.Rect(0, 0, 600, 400)
        self.menu_rect.center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)
        
        self.sub_menu_rect = pygame.Rect(0, 0, 600, 400)
        self.sub_menu_rect.center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)
        
        self.buttons = self.create_buttons()
        self.sub_buttons = self.create_sub_menu_buttons()

    def create_buttons(self):
        
        buttons = {
            "Terrorists": pygame.Rect(0, 0, 300, 50),
            "Counter-Terrorists": pygame.Rect(0, 0, 300, 50),
            "Close": pygame.Rect(0, 0, 300, 50),
        }

        
        y_start = self.menu_rect.top + 50
        for i, rect in enumerate(buttons.values()):
            rect.centerx = self.menu_rect.centerx
            rect.y = y_start + i * 70 

        return buttons

    def create_sub_menu_buttons(self):
        
        sub_buttons = {
            "Phoenix Connexion": pygame.Rect(0, 0, 300, 50),
            "L337 Krew": pygame.Rect(0, 0, 300, 50),
            "Arctic Avengers": pygame.Rect(0, 0, 300, 50),
            "Guerilla Warfare": pygame.Rect(0, 0, 300, 50),
            "Auto-Select": pygame.Rect(0, 0, 300, 50),
        }
        y_start = self.menu_rect.top + 50
        for i, rect in enumerate(sub_buttons.values()):
            rect.centerx = self.menu_rect.centerx
            rect.y = y_start + i * 60
        return sub_buttons

    def toggle(self):
        self.active = not self.active
        self.sub_menu_active = not self.sub_menu_active

    def draw(self):
        if self.active:
            self.draw_main_menu()
            if self.sub_menu_active:
                self.toggle()
                self.draw_sub_menu()

    def draw_main_menu(self):
            
            s = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
            s.set_alpha(0)  
            s.fill((190,158,108))
            self.display_surface.blit(s, (0, 0))

            
            menu_surface = pygame.Surface(self.menu_rect.size)
            menu_surface.fill((50, 50, 50)) 
            menu_surface.set_alpha(128)  
            
            
            self.display_surface.blit(menu_surface, self.menu_rect.topleft)

            
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.menu_rect, 2, border_radius=10)

            mouse_pos = pygame.mouse.get_pos()
            for name, rect in self.buttons.items():
                color = (100, 100, 100)  
                if rect.collidepoint(mouse_pos):
                    color = (150, 150, 150)

                pygame.draw.rect(self.display_surface, color, rect, border_radius=5)
                text_surf = self.font.render(name, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=rect.center)
                self.display_surface.blit(text_surf, text_rect)
    def draw_sub_menu(self):
            
            s = pygame.Surface((self.display_surface.get_width(), self.display_surface.get_height()))
            s.set_alpha(0) 
            s.fill((190,158,108))
            self.display_surface.blit(s, (0, 0))

            
            menu_surface = pygame.Surface(self.sub_menu_rect.size)
            menu_surface.fill((50, 50, 50)) 
            menu_surface.set_alpha(128)  
            
            
            self.display_surface.blit(menu_surface, self.sub_menu_rect.topleft)

            
            pygame.draw.rect(self.display_surface, (255, 255, 255), self.sub_menu_rect, 2, border_radius=10)

           
            mouse_pos = pygame.mouse.get_pos()
            for name, rect in self.sub_buttons.items():
                color = (100, 100, 100)  
                if rect.collidepoint(mouse_pos):
                    color = (150, 150, 150)

                pygame.draw.rect(self.display_surface, color, rect, border_radius=5)
                text_surf = self.font.render(name, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=rect.center)
                self.display_surface.blit(text_surf, text_rect)
