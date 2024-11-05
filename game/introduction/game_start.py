
import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Giao Diện Pygame")

# Định nghĩa màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (10, 10, 50)

# Tạo hàm để vẽ văn bản
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Vòng lặp chính
running = True
font = pygame.font.SysFont("Arial", 30)
while running:
    screen.fill(DARK_BLUE)  # Đặt nền tối màu xanh đậm

    # Vẽ thanh màu vàng trên cùng
    pygame.draw.rect(screen, YELLOW, (0, 0, screen_width, 50))

    # Vẽ tiêu đề
    draw_text("Unreal Software's CS2D", font, WHITE, screen, 20, 60)

    # Vẽ các tùy chọn menu
    menu_options = [
        "Quick Play", "New Game", "Find Servers",
        "Options", "Friends", "Mods",
        "Editor", "Help", "Discord", "Quit"
    ]
    y_offset = 120
    for option in menu_options:
        draw_text(option, font, WHITE, screen, 20, y_offset)
        y_offset += 40

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát Pygame
pygame.quit()
sys.exit()