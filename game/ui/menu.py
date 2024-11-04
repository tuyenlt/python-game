import pygame

class Menu:
	# def draw(self, surface):
	# 	action = False
	# 	#get mouse position
	# 	pos = pygame.mouse.get_pos()

	# 	#check mouseover and clicked conditions
	# 	if self.rect.collidepoint(pos):
	# 		if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
	# 			self.clicked = True
	# 			action = True

	# 	if pygame.mouse.get_pressed()[0] == 0:
	# 		self.clicked = False

	# 	#draw button on screen
	# 	surface.blit(self.image, (self.rect.x, self.rect.y))

	# 	return action
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/korean.ttf', 20)  
        self.main_active = True 
        self.terrorists_menu_active = False
        self.counter_terrorists_menu_active = False
        
        self.menu_rect = pygame.Rect(0, 0, 600, 400)
        self.menu_rect.center = (self.display_surface.get_width() // 2, self.display_surface.get_height() // 2)

        self.main_buttons = self.create_main_buttons()
        self.terrorists_buttons = self.create_terrorists_menu_buttons()
        self.counter_terrorists_buttons = self.create_counter_terrorists_menu_buttons()
        
        self.buttons = self.create_main_buttons()
        

    def create_main_buttons(self):
        main_buttons = {
            "Terrorists": pygame.Rect(0, 0, 300, 50),
            "Counter-Terrorists": pygame.Rect(0, 0, 300, 50),
            "Close": pygame.Rect(0, 0, 300, 50),
        }

        
        y_start = self.menu_rect.top + 50
        for i, rect in enumerate(main_buttons.values()):
            rect.centerx = self.menu_rect.centerx
            rect.y = y_start + i * 70 

        return main_buttons

    def create_terrorists_menu_buttons(self):
        
        terrorists_buttons = {
            "Phoenix Connexion": pygame.Rect(0, 0, 300, 50),
            "L337 Krew": pygame.Rect(0, 0, 300, 50),
            "Arctic Avengers": pygame.Rect(0, 0, 300, 50),
            "Guerilla Warfare": pygame.Rect(0, 0, 300, 50),
            "Auto-Select": pygame.Rect(0, 0, 300, 50),
        }
        y_start = self.menu_rect.top + 50
        for i, rect in enumerate(terrorists_buttons.values()):
            rect.centerx = self.menu_rect.centerx
            rect.y = y_start + i * 60
        return terrorists_buttons
        
    def create_counter_terrorists_menu_buttons(self):
        counter_terrorists_buttons = {
            "SEAL Team 6": pygame.Rect(0, 0, 300, 50),
            "GSG 9": pygame.Rect(0, 0, 300, 50),
            "SAS": pygame.Rect(0, 0, 300, 50),
            "GIGN": pygame.Rect(0, 0, 300, 50),
            "Auto-Select": pygame.Rect(0, 0, 300, 50),
        }
        y_start = self.menu_rect.top + 50
        for i, rect in enumerate(counter_terrorists_buttons.values()):
            rect.centerx = self.menu_rect.centerx
            rect.y = y_start + i * 60
        return counter_terrorists_buttons
    def toggle(self):
        self.main_active = not self.main_active
        # self.sub_menu_active = not self.sub_menu_active

    def draw(self):
        if self.main_active:
            self.draw_menu()
            # if self.sub_menu_active:
            #     self.toggle()
            #     self.draw_sub_menu()

    def draw_menu(self):        
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

                pygame.draw.rect(self.display_surface, color, rect, border_radius=10)
                text_surf = self.font.render(name, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=rect.center)
                self.display_surface.blit(text_surf, text_rect)
