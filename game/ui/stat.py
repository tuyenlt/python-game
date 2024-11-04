import pygame

class StatsMenu:
    def __init__(self, width, height):
        # Initialize menu surface
        self.surface = pygame.Surface((width, height))
        self.surface.set_alpha(125)

        self.players_stat = {}

        # Colors and Fonts
        self.BACKGROUND_COLOR = (30, 30, 30)
        self.ROW_COLOR_1 = (50, 50, 50)
        self.ROW_COLOR_2 = (40, 40, 40)
        self.FONT = pygame.font.SysFont('Arial', 24)
        
        self.hidden = True
        

    def update_players_stat(self, players_stat):
        self.players_stat = players_stat

    def show(self):
        self.hidden = False
    
    def hide(self):
        self.hidden = True

    def draw(self, surface, pos):
        if self.hidden:
            return
        self.surface.fill(self.BACKGROUND_COLOR)
        headers = ["Player", "Kills", "Deaths", "Assists", "KDR", "Score"]
        for i, header in enumerate(headers):
            text_surface = self.FONT.render(header, True, (255, 255, 255))
            self.surface.blit(text_surface, (100 + i * 100, 20))

        players = list(self.players_stat.values())
        for i, player in enumerate(players):
            y_offset = 60 + i * 40
            row_color = self.ROW_COLOR_1 if i % 2 == 0 else self.ROW_COLOR_2
            row_background = pygame.Surface((600, 40))
            row_background.fill(row_color)
            self.surface.blit(row_background, (100, y_offset))
            stats = [
                player["id"], str(player["k"]), str(player["d"]),
                str(player["a"]), str(player["KDR"]), str(player["sc"])
            ]
            
            for j, stat in enumerate(stats):
                text_surface = self.FONT.render(stat, True, (255, 255, 255))
                self.surface.blit(text_surface, (100 + j * 100, y_offset))

        surface.blit(self.surface, pos)
