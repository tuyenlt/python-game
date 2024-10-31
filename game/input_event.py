import pygame

class InputEvent():
    def __init__(self):
        self.mouse_clicking = False
        self.on_click_callback = None
        pass
    
    def update_event(self, events : list[pygame.event.EventType]):
        for event in events:
            if event.type ==  pygame.MOUSEBUTTONDOWN:                
                if event.button == 1:
                    self.mouse_clicking = True
                    if self.on_click_callback:
                        self.on_click_callback()
            if event.type ==  pygame.MOUSEBUTTONUP:                
                if event.button == 1:
                    self.mouse_clicking = False
    
    def get_event_input(self, event : pygame.event.EventType):
        pass        
    
    def get_event(self):
        pass