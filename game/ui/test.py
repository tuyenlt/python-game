import pygame
import sys

pygame.init()

# Kích thước màn hình
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu Example")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 200, 255)

# Tạo phông chữ
font = pygame.font.SysFont(None, 40)

# Hàm vẽ nút
def draw_button(text, x, y, w, h, color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, w, h)
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_surface, text_rect)
    return button_rect

# Menu chính và menu phụ
main_menu = True
sub_menu = False

# Vòng lặp chính
running = True
while running:
    screen.fill(BLACK)

    if main_menu:
        title = font.render("Main Menu", True, WHITE)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

        button1 = draw_button("Go to Submenu", 300, 150, 200, 50, BLUE, LIGHT_BLUE)
        button2 = draw_button("Settings", 300, 250, 200, 50, BLUE, LIGHT_BLUE)
        button3 = draw_button("Exit", 300, 350, 200, 50, BLUE, LIGHT_BLUE)

    elif sub_menu:
        title = font.render("Submenu", True, WHITE)
        screen.blit(title, (screen_width // 2 - title.get_width() // 2, 50))

        button_back = draw_button("Back to Main Menu", 300, 250, 200, 50, BLUE, LIGHT_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if main_menu:
                if button1.collidepoint(event.pos):
                    main_menu = False
                    sub_menu = True
                elif button2.collidepoint(event.pos):
                    print("Settings Clicked!")
                elif button3.collidepoint(event.pos):
                    running = False
            elif sub_menu:
                if button_back.collidepoint(event.pos):
                    main_menu = True
                    sub_menu = False

    pygame.display.flip()

pygame.quit()
sys.exit()
