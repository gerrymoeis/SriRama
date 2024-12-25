# enemies.py
# Enemy dengan pola random dan akselerasi

import pygame
import random
from game_objects.base import Entity

class Enemy(Entity):
    def __init__(self, x, y, width, height, color, speed, patrol_range):
        super().__init__(x, y, width, height, color)
        self.speed = speed
        self.patrol_range = patrol_range
        self.start_x = x

    def update(self, players):
        self.patrol()

    def patrol(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.patrol_range:
            self.direction *= -1  # Balik arah


class EnemyRandom(Enemy):
    def __init__(self, x, y, width, height, color, speed, patrol_range):
        super().__init__(x, y, width, height, color, speed, patrol_range)
        self.target_player = None
        self.acceleration = 1.0  # Kecepatan awal
        self.max_speed = speed * 3  # Kecepatan maksimal
    
    def update(self, players):
        if not self.target_player or random.random() < 0.01:  # Pilih target baru
            self.target_player = random.choice(players)
        
        # Mengejar player
        if self.target_player:
            dx = self.target_player.rect.x - self.rect.x
            dy = self.target_player.rect.y - self.rect.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                self.rect.x += self.acceleration * dx / distance
                self.rect.y += self.acceleration * dy / distance
            
            # Akselerasi
            if random.random() < 0.02:  # Peluang akselerasi
                self.acceleration = min(self.acceleration + 0.5, self.max_speed)
            else:
                self.acceleration = max(self.acceleration - 0.1, self.speed)
