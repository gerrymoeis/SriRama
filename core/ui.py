import pygame
from mechanics.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, RED, GREEN

class UI:
    def __init__(self, screen, size=50):
        self.screen = screen
        self.size = size
        self.font = pygame.font.Font(None, self.size)

    def draw_health_bar(self, x, y, width, height, current_hp, max_hp):
        # Hitung panjang bar berdasarkan HP
        hp_percentage = current_hp / max_hp
        bar_width = int(width * hp_percentage)

        # Bar background
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, width, height))
        # Bar foreground
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, bar_width, height))
        # Border
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, width, height), 2)

    def draw_spiritual_bar(self, x, y, width, height, value, max_value):
        # Placeholder Spiritual Bar
        ratio = value / max_value
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 2)  # Border
        pygame.draw.rect(self.screen, GREEN, (x + 2, y + 2, (width - 4) * ratio, height - 4))
    
    def draw_message(self, message, color, x, y):
        text = self.font.render(message, True, color)
        self.screen.blit(text, (x, y))

class PauseMenu:
    def __init__(self, screen, size=50):
        self.screen = screen
        self.size = size
        self.font = pygame.font.Font(None, self.size)

    def draw(self):
        text = self.font.render("PAUSED", True, (0, 0, 0))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - self.size * 1.1, SCREEN_HEIGHT // 2 - self.size * 1.1))