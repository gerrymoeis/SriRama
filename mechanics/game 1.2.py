# game.py
# Modifikasi untuk menambahkan efek damage lebih impactful

import pygame
from mechanics.config import SCREEN_WIDTH, SCREEN_HEIGHT, RED, BLUE, GREEN, WHITE
from game_objects.characters import Player
from game_objects.enemies import Enemy

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.players = [
            Player("Sri", (100, 100), controls="WASD", color=BLUE),
            Player("Rama", (200, 200), controls="ARROWS", color=RED)
        ]
        self.enemies = pygame.sprite.Group(
            Enemy(400, 300, 40, 40, (150, 0, 0), 2, 100)  # Contoh enemy
        )
        self.shake_intensity = 0
        self.damage_cooldown = 0  # Untuk delay damage per frame
    
    def update(self):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        for player in self.players:
            player.update()
        
        for enemy in self.enemies:
            enemy.update(self.players)  # Enemy mengejar player
        
        self.check_collisions()

    def check_collisions(self):
        for enemy in self.enemies:
            for player in self.players:
                if player.rect.colliderect(enemy.rect) and self.damage_cooldown == 0:
                    player.hp -= 10  # Kurangi HP
                    player.color = (255, 200, 200)  # Indikator warna
                    self.shake_intensity = 10  # Intensitas getaran
                    self.damage_cooldown = 60  # Delay 1 detik (FPS=60)

    def draw(self):
        # Efek getaran layar
        if self.shake_intensity > 0:
            offset_x = pygame.time.get_ticks() % self.shake_intensity - self.shake_intensity // 2
            offset_y = pygame.time.get_ticks() % self.shake_intensity - self.shake_intensity // 2
            self.shake_intensity = max(self.shake_intensity - 1, 0)
        else:
            offset_x, offset_y = 0, 0

        self.screen.fill(WHITE)
        for player in self.players:
            player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
