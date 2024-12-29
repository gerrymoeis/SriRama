import math, pygame
from game_objects.base import Entity

from mechanics.config import RED, BLUE

from core.animation import Animation

class Character(Entity):
    def __init__(self, x, y, width, height, speed, screen, color, animations):
        super().__init__(x, y, width, height, color, animations)
        self.speed = speed
        self.screen = screen
        self.default_color = color  # Warna awal

        self.skill_active = False
        self.skill_cooldown = 0
        self.skill_timer = 0
        self.skill_duration = 0

        self.invisible = False

    def move(self, keys, up, down, left, right):
        if keys[up]:
            self.image_rect.y -= self.speed
        if keys[down]:
            self.image_rect.y += self.speed
        if keys[left]:
            self.image_rect.x -= self.speed
        if keys[right]:
            self.image_rect.x += self.speed
    
    def update_skill(self, current_time):
        """Update mekanik skill, logika spesifik diterapkan di subclass."""
        if self.skill_active:
            if current_time - self.skill_timer >= self.skill_duration:
                self.skill_active = False
                self.reset_after_skill()

        if self.skill_cooldown > 0:
            self.skill_cooldown -= 20
    
class Sri(Character):
    def __init__(self, x, y, width, height, speed, screen, color=BLUE):
        animations = {
            "idle": Animation("assets/images/characters/The Female Adventurer/Idle/idle.png", 48, 64, 8, 5, 3),
            "walk": Animation("assets/images/characters/The Female Adventurer/Walk/walk.png", 48, 64, 8, 10, 3),
            "run": Animation("assets/images/characters/The Female Adventurer/Dash/dash.png", 48, 64, 8, 15, 3),
        }
        
        super().__init__(x, y, width, height, speed, screen, color, animations)
        self.name = "Sri"

    def activate_skill(self):
        if self.skill_cooldown <= 0:  # Hanya bisa digunakan jika tidak dalam cooldown
            self.skill_active = True
            self.speed *= 2  # Percepatan movement speed
            self.color = (173, 216, 230)  # Biru muda sebagai indikator
            self.skill_duration = 3000  # Durasi 3 detik
            self.skill_timer = pygame.time.get_ticks()
            self.skill_cooldown = 9000  # Cooldown 9 detik

            self.invisible = True

    def create_dash_area(self):
        """Buat area dash dan knockback musuh."""
        radius = 50  # Placeholder radius lingkaran
        pygame.draw.circle(self.screen, (0, 0, 255), (int(self.image_rect.x) + self.image_rect.width // 2, int(self.image_rect.y) + self.image_rect.height // 2), radius, 2)
    
    def reset_after_skill(self):
        self.speed /= 2  # Kembalikan kecepatan semula
        self.color = (0, 0, 255)  # Kembali ke warna biru asli
        self.invisible = False


class Rama(Character):
    def __init__(self, x, y, width, height, speed, screen, color=RED):
        animations = {
            "idle": Animation("assets/images/characters/The Adventurer/Idle/idle.png", 48, 64, 8, 5, 3),
            "walk": Animation("assets/images/characters/The Adventurer/Walk/walk.png", 48, 64, 8, 10, 3),
        }

        super().__init__(x, y, width, height, speed, screen, color, animations)
        self.name = "Rama"
        
    def activate_skill(self):
        if self.skill_cooldown <= 0:  # Hanya bisa digunakan jika tidak dalam cooldown
            self.skill_active = True
            self.skill_duration = 5000  # Durasi 5 detik
            self.skill_timer = pygame.time.get_ticks()
            self.skill_cooldown = 12000  # Cooldown 12 detik

    def create_healing_area(self, enemies):
        """Buat area healing dan knockback musuh."""
        radius = 200  # Placeholder radius lingkaran
        pygame.draw.circle(self.screen, (255, 255, 0), (int(self.image_rect.x) + self.image_rect.width // 2, int(self.image_rect.y) + self.image_rect.height // 2), radius, 2)

        # Knockback logic
        for enemy in enemies:  # `enemies` adalah daftar objek musuh dalam game
            dx = enemy.image_rect.x - self.image_rect.x
            dy = enemy.image_rect.y - self.image_rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance < radius:
                knockback_force = 10
                angle = math.atan2(dy, dx)
                enemy.image_rect.x += math.cos(angle) * knockback_force
                enemy.image_rect.y += math.sin(angle) * knockback_force
                
    def reset_after_skill(self):
        # Tidak ada perubahan langsung untuk Rama setelah skill selesai
        pass
