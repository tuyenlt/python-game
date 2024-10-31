import pygame


class Button:
    def __init__(self, pos, size, text, color, call_back):
        self.pos_x , self.pos_y = pos
        self.width, self.height = size
        self.text = text
        self.call_back = call_back
        self.color = color
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        
    def listen(self, events : list[pygame.event.EventType]):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(mouse_x, mouse_y):
                    self.call_back()
    
    def display(self, surf):
        pygame.draw.rect(surf, (self.color), self.rect)
    
        
        