import pygame

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 215, 0)  # Warna koin (emas)
        self.radius = 10  # Ukuran koin

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def collides_with(self, character):
        """Periksa apakah koin dikumpulkan oleh karakter."""
        distance = ((self.x - character.x)**2 + (self.y - character.y)**2)**0.5
        return distance < self.radius + character.width // 2