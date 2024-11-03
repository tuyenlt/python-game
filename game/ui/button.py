import pygame


class UIComponent:
    
    mouse_clicked = False
    mouse_clicking = False
    mouse_x = 0
    mouse_y = 0
    
    @classmethod
    def event_listen(cls, events : list[pygame.event.EventType]):
        (cls.mouse_x, cls.mouse_y) = pygame.mouse.get_pos()
        cls.mouse_clicked = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                cls.mouse_click = True
                cls.mouse_clicking = True
            if event.type == pygame.MOUSEBUTTONUP:
                cls.mouse_clicking = False
        

    def __init__(self, pos, size):
        self.pos_x , self.pos_y = pos
        self.width, self.height = size
    
    def update(self):
        pass
    
class Label(UIComponent):
    def __init__(self):
        pass

class Button(UIComponent):
    def __init__(self, pos, size, text, color, click_cb, radius = 0):
        super().__init__(pos, size)
        self.font = pygame.font.Font('assets/fonts/korean.ttf', 20)
        self.text = text
        self.click_cb = click_cb
        self.on_hover_color = color
        self.off_hover_color = (150, 150, 150)
        self.color = self.off_hover_color
        self.radius = radius
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.on_hover = None
        self.width = 0
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
        self.click_cnt = 0
        
    def update(self):
        if self.rect.collidepoint(self.mouse_x, self.mouse_y):
            self.on_hover()
            if self.mouse_clicking:
                self.click_cb()
                self.click_cnt += 1
        self.display()        
        
    def on_hover(self):
        self.color = self.on_hover_color
    
    def off_hover(self):
        self.color = self.off_hover_color
        
    
    def display(self):
        pygame.draw.rect(self.surf, (self.color), self.rect, self.width, self.radius)
        self.surf.blit(self.text_rect, self.text_surf)
    
        
        