import pygame

class Intro:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.background = pygame.transform.scale(pygame.image.load('assets/intro/CS2D.png'), (1280, 720)).convert()
        self.background_rect = self.background.get_rect()

        
        self.font = pygame.font.Font('assets/fonts/UI_font.ttf', 30)  
        self.text_color = (0, 0, 0)
        self.text = self.font.render("Press anywhere to continue", True, self.text_color)
        self.text_rect = self.text.get_rect(center=(640, 560))

       
        self.alpha_surface = pygame.Surface((self.text_rect.width + 20, self.text_rect.height + 20))
        self.alpha_surface.set_alpha(128) 
        self.alpha_surface.fill((255, 255, 255))

        
        self.blink = True
        self.blink_interval = 0.4  
        self.last_blink_time = pygame.time.get_ticks() / 1000
        
        self.intro_menu_active = True

    def draw(self):
        if self.intro_menu_active :
            cur = pygame.time.get_ticks() / 1000
            if cur - self.last_blink_time >= self.blink_interval:
                self.blink = not self.blink
                self.last_blink_time = cur

            
            self.display_surface.blit(self.background, (0, 0))

            
            alpha_rect = self.alpha_surface.get_rect(center=self.text_rect.center)
            self.display_surface.blit(self.alpha_surface, alpha_rect)

        
            if self.blink:
                self.display_surface.blit(self.text, self.text_rect)
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.intro_menu_active:
            mouse_pos = pygame.mouse.get_pos()
            if self.background_rect.collidepoint(mouse_pos):
                self.intro_menu_active = False