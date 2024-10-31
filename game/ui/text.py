import pygame

# Khởi tạo Pygame
pygame.init()

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Cỡ màn hình
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Lớp Text
class Text:
    def __init__(self, text, color):
        self.text = text
        self.color = color
        self.font = pygame.font.Font('assets/fonts/digital-7.ttf', 20)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()

    def draw(self, surface, pos):
        self.rect.topleft = pos
        surface.blit(self.image, self.rect)

# Lớp Button
class Button:
    def __init__(self, text, pos, size, bg_color=GRAY, text_color=BLACK):
        self.rect = pygame.Rect(pos, size)
        self.bg_color = bg_color
        self.hover_color = (min(self.bg_color[0] + 30, 255), 
                            min(self.bg_color[1] + 30, 255), 
                            min(self.bg_color[2] + 30, 255))  # Màu khi hover
        self.current_color = self.bg_color
        self.text = Text(text, text_color)
        # Căn giữa chữ trên button
        self.text.rect.center = self.rect.center

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        self.text.draw(surface, self.text.rect.topleft)

    def handle_event(self, event):
        # Thay đổi màu khi hover và check click
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.current_color = self.hover_color
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(f"Button {self.text.text} clicked!")  # Xử lý click
                return True
        else:
            self.current_color = self.bg_color
        return False

# Màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu Example")

# Tạo button với kích thước cụ thể
play_button = Button("Play", (300, 200), (200, 50))
quit_button = Button("Quit", (300, 300), (200, 50))

# Vòng lặp game
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if play_button.handle_event(event):
            print("Play button pressed")
        if quit_button.handle_event(event):
            running = False  # Dừng vòng lặp khi nút Quit được nhấn

    # Vẽ button
    play_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.flip()

pygame.quit()
