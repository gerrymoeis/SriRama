import pygame

class Entity:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, offset=(0, 0)):
        self.rect.x += offset[0]
        self.rect.y += offset[1]
        pygame.draw.rect(screen, self.color, self.rect)