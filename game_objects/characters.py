import math, pygame
from game_objects.base import Entity

from mechanics.config import RED, BLUE

class Character(Entity):
    def __init__(self, x, y, width, height, speed, screen, color):
        super().__init__(x, y, width, height, color)
        self.speed = speed
        self.screen = screen
        self.default_color = color  # Warna awal

        self.skill_active = False
        self.skill_cooldown = 0
        self.skill_timer = 0
        self.skill_duration = 0

    def move(self, keys, up, down, left, right):
        if keys[up]:
            self.rect.y -= self.speed
        if keys[down]:
            self.rect.y += self.speed
        if keys[left]:
            self.rect.x -= self.speed
        if keys[right]:
            self.rect.x += self.speed
    
    def update_skill(self, current_time):
        """Update mekanik skill, logika spesifik diterapkan di subclass."""
        if self.skill_active:
            if current_time - self.skill_timer >= self.skill_duration:
                self.skill_active = False
                self.reset_after_skill()

        if self.skill_cooldown > 0:
            self.skill_cooldown -= 25
    
class Sri(Character):
    def __init__(self, x, y, width, height, speed, screen, color=BLUE):
        super().__init__(x, y, width, height, speed, screen, color)
        self.name = "Sri"

    def activate_skill(self):
        if self.skill_cooldown == 0:  # Hanya bisa digunakan jika tidak dalam cooldown
            self.skill_active = True
            self.speed *= 2  # Percepatan movement speed
            self.color = (173, 216, 230)  # Biru muda sebagai indikator
            self.skill_duration = 3000  # Durasi 3 detik
            self.skill_timer = pygame.time.get_ticks()
            self.skill_cooldown = 10000  # Cooldown 10 detik

    def reset_after_skill(self):
        self.speed /= 2  # Kembalikan kecepatan semula
        self.color = (0, 0, 255)  # Kembali ke warna biru asli


class Rama(Character):
    def __init__(self, x, y, width, height, speed, screen, color=RED):
        super().__init__(x, y, width, height, speed, screen, color)
        self.name = "Rama"
        
    def activate_skill(self):
        if self.skill_cooldown == 0:  # Hanya bisa digunakan jika tidak dalam cooldown
            self.skill_active = True
            self.skill_duration = 5000  # Durasi 5 detik
            self.skill_timer = pygame.time.get_ticks()
            self.skill_cooldown = 12000  # Cooldown 12 detik

    def create_healing_area(self, enemies):
        """Buat area healing dan knockback musuh."""
        radius = 200  # Placeholder radius lingkaran
        pygame.draw.circle(self.screen, (255, 255, 0), (int(self.rect.x) + self.rect.width // 2, int(self.rect.y) + self.rect.height // 2), radius, 2)

        # Knockback logic
        for enemy in enemies:  # `enemies` adalah daftar objek musuh dalam game
            dx = enemy.rect.x - self.rect.x
            dy = enemy.rect.y - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance < radius:
                knockback_force = 10
                angle = math.atan2(dy, dx)
                enemy.rect.x += math.cos(angle) * knockback_force
                enemy.rect.y += math.sin(angle) * knockback_force
                
    def reset_after_skill(self):
        # Tidak ada perubahan langsung untuk Rama setelah skill selesai
        pass
