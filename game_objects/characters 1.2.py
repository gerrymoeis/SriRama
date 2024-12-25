import pygame
from game_objects.base import Entity

# characters.py
class Player(pygame.sprite.Sprite):
    def __init__(self, name, position, controls="WASD", color=(0, 255, 0)):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)
        self.speed = 5
        self.hp = 100
        self.controls = controls
        self.default_color = color  # Warna awal

    def update(self):
        keys = pygame.key.get_pressed()
        # Pergerakan
        ...

        # Reset warna
        if self.image.get_at((0, 0)) != self.default_color:
            self.image.fill(self.default_color)
