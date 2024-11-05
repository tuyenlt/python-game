import pygame

COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_INACTIVE = pygame.Color('gray15')
FONT_COLOR = pygame.Color('white')

class InputBox:
    def __init__(self, x, y, w, h, limit = 50):
        self.width = w
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = ''
        self.FONT = pygame.font.Font(None, 32)
        self.txt_surface = self.FONT.render(self.text, True, FONT_COLOR)
        self.active = False
        self.limit = limit

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Kiểm tra xem có click vào ô nhập không
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.text.__len__() < self.limit:
                        self.text += event.unicode
                self.txt_surface = self.FONT.render(self.text, True, FONT_COLOR)
                
    def draw(self, screen):
        # Vẽ văn bản
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Vẽ hình chữ nhật của ô nhập