import pygame

class UI:
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('assets/fonts/digital-7.ttf', 60)
    
    def show_hp(self, hp):
        # Tạo surface để hiển thị HP
        text_render = self.font.render(str(int(hp)), False, (255,232,80))
        text_rect = text_render.get_rect()

        # Vị trí hiển thị
        x =  20  # Căn bên phải
        y = self.display_surface.get_size()[1] - text_rect.height - 20  # Căn dưới
        text_rect.topleft = (x, y)

        # Vẽ chữ lên màn hình
        self.display_surface.blit(text_render, text_rect)

        # pygame.draw.rect(self.display_surface, 'black', text_rect.inflate(30, 15), border_radius=5)

    def display(self, player):
        self.show_hp(player.hp)
