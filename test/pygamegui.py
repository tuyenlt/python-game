import pygame
import pygame_gui

class Menu:
    def __init__(self, manager):
        self.manager = manager
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../assets/fonts/korean.ttf', 20)
        
        # Flags for active menu
        self.main_active = True
        self.terrorists_menu_active = False
        self.counter_terrorists_menu_active = False
        
        # Create UI containers for each menu section
        self.main_container = pygame_gui.core.UIContainer(
            pygame.Rect(100, 100, 600, 400), manager=manager, anchors={'center': 'center'}
        )
        self.terrorists_container = pygame_gui.core.UIContainer(
            pygame.Rect(100, 100, 600, 400), manager=manager, anchors={'center': 'center'}
        )
        self.counter_terrorists_container = pygame_gui.core.UIContainer(
            pygame.Rect(100, 100, 600, 400), manager=manager, anchors={'center': 'center'}
        )
        
        # Create buttons in each container
        self.create_main_buttons()
        self.create_terrorists_menu_buttons()
        self.create_counter_terrorists_menu_buttons()
        
        # Set initial visibility
        self.terrorists_container.hide()
        self.counter_terrorists_container.hide()

    def create_main_buttons(self):
        # Main menu buttons
        self.main_buttons = {
            "Terrorists": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 50, 300, 50),
                text="Terrorists",
                manager=self.manager,
                container=self.main_container
            ),
            "Counter-Terrorists": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 130, 300, 50),
                text="Counter-Terrorists",
                manager=self.manager,
                container=self.main_container
            ),
            "Close": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 210, 300, 50),
                text="Close",
                manager=self.manager,
                container=self.main_container
            )
        }

    def create_terrorists_menu_buttons(self):
        # Terrorists menu buttons
        self.terrorists_buttons = {
            "Phoenix Connexion": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 50, 300, 50),
                text="Phoenix Connexion",
                manager=self.manager,
                container=self.terrorists_container
            ),
            "L337 Krew": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 110, 300, 50),
                text="L337 Krew",
                manager=self.manager,
                container=self.terrorists_container
            ),
            "Arctic Avengers": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 170, 300, 50),
                text="Arctic Avengers",
                manager=self.manager,
                container=self.terrorists_container
            ),
            "Guerilla Warfare": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 230, 300, 50),
                text="Guerilla Warfare",
                manager=self.manager,
                container=self.terrorists_container
            ),
            "Auto-Select": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 290, 300, 50),
                text="Auto-Select",
                manager=self.manager,
                container=self.terrorists_container
            )
        }

    def create_counter_terrorists_menu_buttons(self):
        # Counter-terrorists menu buttons
        self.counter_terrorists_buttons = {
            "SEAL Team 6": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 50, 300, 50),
                text="SEAL Team 6",
                manager=self.manager,
                container=self.counter_terrorists_container
            ),
            "GSG 9": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 110, 300, 50),
                text="GSG 9",
                manager=self.manager,
                container=self.counter_terrorists_container
            ),
            "SAS": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 170, 300, 50),
                text="SAS",
                manager=self.manager,
                container=self.counter_terrorists_container
            ),
            "GIGN": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 230, 300, 50),
                text="GIGN",
                manager=self.manager,
                container=self.counter_terrorists_container
            ),
            "Auto-Select": pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(150, 290, 300, 50),
                text="Auto-Select",
                manager=self.manager,
                container=self.counter_terrorists_container
            )
        }

    def toggle_menu(self, menu_name):
        # Toggle visibility of menus based on menu_name
        if menu_name == "Terrorists":
            self.main_container.hide()
            self.terrorists_container.show()
            self.counter_terrorists_container.hide()
        elif menu_name == "Counter-Terrorists":
            self.main_container.hide()
            self.counter_terrorists_container.show()
            self.terrorists_container.hide()
        elif menu_name == "Close":
            self.main_container.hide()
            self.terrorists_container.hide()
            self.counter_terrorists_container.hide()
        else:
            self.main_container.show()
            self.terrorists_container.hide()
            self.counter_terrorists_container.hide()

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.main_buttons["Terrorists"]:
                self.toggle_menu("Terrorists")
            elif event.ui_element == self.main_buttons["Counter-Terrorists"]:
                self.toggle_menu("Counter-Terrorists")
            elif event.ui_element == self.main_buttons["Close"]:
                self.toggle_menu("Close")
            for index, button in enumerate(self.terrorists_buttons):
                if event.ui_element == self.terrorists_buttons[button]:
                    print("t",index + 1)
                    self.toggle_menu("Close")
            for index, button in enumerate(self.counter_terrorists_buttons):
                if event.ui_element == self.counter_terrorists_buttons[button]:
                    print("ct", index + 1)
                    self.toggle_menu("Close")
                    


# Initialize Pygame and Pygame GUI
pygame.init()
pygame.display.set_caption("Pygame GUI Menu Example")
screen = pygame.display.set_mode((800, 600))

# Pygame GUI Manager
manager = pygame_gui.UIManager((800, 600))

# Create Menu instance
menu = Menu(manager)

clock = pygame.time.Clock()

# Main loop
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Pass events to the GUI manager and menu
        manager.process_events(event)
        menu.handle_event(event)

    # Update GUI manager
    manager.update(time_delta)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_m]:
        menu.toggle_menu("main")
    # Draw everything
    screen.fill((200, 200, 200))
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
