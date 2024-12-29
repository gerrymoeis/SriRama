import random
import pygame

from game_objects.base import Entity

class Enemy(Entity):
    def __init__(self, x, y, width, height, color, speed, patrol_range, animations):
        super().__init__(x, y, width, height, color, animations)
        self.speed = speed
        self.patrol_range = patrol_range
        self.direction = 1  # 1 untuk maju, -1 untuk mundur
        self.start_x = x
        
    def patrol_horizontal(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.patrol_range:
            self.direction *= -1  # Balik arah
    
    def chase(self):
        self.patrol_horizontal()

class EnemyRandom(Enemy):
    def __init__(self, x, y, width, height, color, speed, patrol_range, animations):
        super().__init__(x, y, width, height, color, speed, patrol_range, animations)
        self.target_player = None
        self.acceleration = 2.0  # Kecepatan awal
        self.max_speed = speed * 4  # Kecepatan maksimal

        self.image_for_rect = pygame.transform.scale(self.image, (48, 48))
        self.image_rect = self.image_for_rect.get_rect(topleft=(x, y))
    
    def draw(self, screen, offset=(0, 0)):
        """Menggambar sprite ke layar."""
        # pygame.draw.rect(screen, (0, 0, 0), self.image_rect)
        
        self.image_rect.x += offset[0]
        self.image_rect.y += offset[1]
        screen.blit(self.image, (self.image_rect.x - 32 // 2.25, self.image_rect.y - 32 // 1.75))
    
    def chase(self, players):
        if not self.target_player or random.random() < 0.01:  # Pilih target baru
            self.target_player = random.choice(players)
        
        # Mengejar player
        if self.target_player:
            dx = self.target_player.image_rect.x - self.image_rect.x
            dy = self.target_player.image_rect.y - self.image_rect.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                self.image_rect.x += self.acceleration * dx / distance
                self.image_rect.y += self.acceleration * dy / distance
            
            # Akselerasi
            if random.random() < 0.005:  # Peluang akselerasi
                self.acceleration = min(self.acceleration + 0.5, self.max_speed)
            else:
                self.acceleration = max(self.acceleration - 0.1, self.speed)
            
            # Deselerasi
            if random.random() < 0.005:  # Peluang deselerasi
                self.acceleration = min(self.acceleration + 0.5, self.max_speed)
            else:
                self.acceleration = max(self.acceleration - 0.1, self.speed)