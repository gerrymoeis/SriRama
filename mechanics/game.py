import pygame
import random

from mechanics.config import SCREEN_WIDTH, SCREEN_HEIGHT, RED, BLUE, GREEN
from game_objects.characters import Sri, Rama
from game_objects.enemies import EnemyRandom
from core.ui import UI, PauseMenu, GameOver, SkillCooldownUI

class Game:
    def __init__(self, screen):
        self.screen = screen
        
        self.enemies = []
        self.max_hp = 100
        self.hp = self.max_hp
        self.all_sprites = []

        self.ui = UI(screen)
        self.pause_menu = PauseMenu(screen)
        self.paused = False
        self.game_over = GameOver(screen)
        
        self.shake_intensity = 0
        self.damage_cooldown = 0
        self.spiritual_bar = 50
        self.max_spiritual_bar = 100

        self.enemy_spawn_time = 2000  # Spawn setiap 2 detik
        self.last_spawn_time = pygame.time.get_ticks()

        self.players = [
            Sri(100, 100, 40, 40, 5, self.screen),
            Rama(200, 100, 40, 40, 5, self.screen)
        ]
        self.sri_ui = SkillCooldownUI(self.screen, self.players[0], BLUE, (SCREEN_WIDTH - 200, 50))
        self.rama_ui = SkillCooldownUI(self.screen, self.players[1], RED, (SCREEN_WIDTH - 200, 100))

        self.reset_game()

    def reset_game(self):
        """Reset state game dengan randomisasi untuk posisi, jumlah enemy, dan atribut lainnya."""
        self.players = [
            Sri(100, 100, 40, 40, 5, self.screen),
            Rama(200, 100, 40, 40, 5, self.screen)
        ]

        self.sri_ui = SkillCooldownUI(self.screen, self.players[0], BLUE, (SCREEN_WIDTH - 200, 50))
        self.rama_ui = SkillCooldownUI(self.screen, self.players[1], RED, (SCREEN_WIDTH - 200, 100))

        # Randomisasi jumlah musuh antara 3-6
        num_enemies = random.randint(3, 6)
        self.enemies = [
            EnemyRandom(
                random.randint(0, SCREEN_WIDTH - 50),
                random.randint(-50, -25),
                40, 40,
                (0, random.randint(100, 255), 0),  # Hijau acak untuk warna
                random.randint(1, 3),  # Kecepatan acak
                random.randint(50, 150)  # HP acak
            ) for _ in range(num_enemies)
        ]

        self.hp = self.max_hp
        self.spiritual_bar = 50
        self.all_sprites = self.players + self.enemies
        self.shake_intensity = 0
        self.damage_cooldown = 0

        self.unpause_game()

    def scale_objects(self, new_resolution):
        """Melakukan scaling objek berdasarkan resolusi layar baru."""
        width_ratio = new_resolution[0] / self.current_resolution[0]
        height_ratio = new_resolution[1] / self.current_resolution[1]

        for player in self.players:
            player.rect.x = int(player.rect.x * width_ratio)
            player.rect.y = int(player.rect.y * height_ratio)
            player.rect.width = int(player.rect.width * width_ratio)
            player.rect.height = int(player.rect.height * height_ratio)

        for enemy in self.enemies:
            enemy.rect.x = int(enemy.rect.x * width_ratio)
            enemy.rect.y = int(enemy.rect.y * height_ratio)
            enemy.rect.width = int(enemy.rect.width * width_ratio)
            enemy.rect.height = int(enemy.rect.height * height_ratio)

        self.current_resolution = new_resolution

    def prevent_player_out_of_bounds(self):
        """Mencegah player keluar dari layar."""
        for player in self.players:
            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.right > SCREEN_WIDTH:
                player.rect.right = SCREEN_WIDTH
            if player.rect.top < 0:
                player.rect.top = 0
            if player.rect.bottom > SCREEN_HEIGHT:
                player.rect.bottom = SCREEN_HEIGHT
    
    def spawn_enemy(self):
        """Spawn enemy secara random dari sisi-sisi batas layar."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.enemy_spawn_time:
            spawn_side = random.choice(['top', 'bottom', 'left', 'right'])
            if spawn_side == 'top':
                x = random.randint(0, SCREEN_WIDTH)
                y = -50  # Spawn di luar layar bagian atas
            elif spawn_side == 'bottom':
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT + 50  # Spawn di luar layar bagian bawah
            elif spawn_side == 'left':
                x = -50  # Spawn di luar layar bagian kiri
                y = random.randint(0, SCREEN_HEIGHT)
            elif spawn_side == 'right':
                x = SCREEN_WIDTH + 50  # Spawn di luar layar bagian kanan
                y = random.randint(0, SCREEN_HEIGHT)
            
            num_enemies = random.randint(1, 3)
            for _ in range(num_enemies):
                new_enemy = EnemyRandom(
                    x, y, 40, 40,
                    (0, random.randint(100, 255), 0),  # Hijau acak untuk warna
                    random.randint(1, 3),  # Kecepatan acak
                    random.randint(50, 150))  # HP acak
                
                self.enemies.append(new_enemy)
                self.all_sprites.append(new_enemy)
                self.last_spawn_time = current_time

    def pause_game(self):
        self.paused = True
    
    def unpause_game(self):
        self.paused = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        controls = [
            (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d),
            (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        ]
        for player, control in zip(self.players, controls):
            player.move(keys, *control)

    def check_collisions(self):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

        for player in self.players:
            for enemy in self.enemies:
                if player.rect.colliderect(enemy.rect) and self.damage_cooldown == 0:
                    self.hp -= 5
                    player.color = (0, 0, 0)
                    self.shake_intensity = 20
                    self.damage_cooldown = 30

                    self.draw()

    def check_game_over(self):
        if self.hp <= 0:
            return "LOSE"
        if not self.enemies:
            return "WIN"
        return None

    def handle_spiritual_mechanics(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.spiritual_bar = min(self.max_spiritual_bar, self.spiritual_bar + 1)

    def draw_ui(self):
        self.ui.draw_health_bar(10, 10, 200, 20, self.hp, self.max_hp)
        self.ui.draw_spiritual_bar(10, 40, 200, 20, self.spiritual_bar, self.max_spiritual_bar)

        [sri, rama] = self.players
        self.sri_ui.draw("Sri", sri.skill_cooldown)
        self.rama_ui.draw("Rama", rama.skill_cooldown)

    def apply_shake_effect(self):
        if self.shake_intensity > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity = max(self.shake_intensity - 1, 0)
            return offset_x, offset_y
        return 0, 0

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.paused:
            last_input_time = 0
            
            if current_time - last_input_time > 50:
                self.pause_menu.draw()
            
            self.last_input_time = current_time  # Reset cooldown
        else:
            game_state = self.check_game_over()
            if game_state == "LOSE":
                last_input_time = 0
                
                if current_time - last_input_time > 50:
                    self.game_over.draw()
                self.last_input_time = current_time  # Reset cooldown
            elif game_state == "WIN":
                self.ui.draw_message("YOU WIN!", GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                return
            else:
                self.handle_input()
                self.prevent_player_out_of_bounds()
                self.check_collisions()
                self.handle_spiritual_mechanics()
                
                self.spawn_enemy()

                for enemy in self.enemies:
                    enemy.chase(self.players)

                for player in self.players:
                    player.color = player.default_color
                    player.update_skill(current_time)
                
                # Handle input untuk skill
                [sri, rama] = self.players
                keys = pygame.key.get_pressed()
                if keys[pygame.K_f]:  # Aktivasi skill untuk Sri
                    sri.activate_skill()
                if keys[pygame.K_RSHIFT]:  # Aktivasi skill untuk Rama
                    rama.activate_skill()
                
                if rama.skill_active:
                    rama.create_healing_area(self.enemies)  # Tampilkan area healing selama skill aktif
                    self.hp += 0.5
                
                if self.hp >= self.max_hp:
                    self.hp = self.max_hp
                
                for sprite in self.all_sprites:
                    sprite.draw(self.screen)
                
                self.draw_ui()

    def draw(self):
        offset_x, offset_y = self.apply_shake_effect()
        self.screen.fill((255, 255, 255))
        for sprite in self.all_sprites:
            sprite.draw(self.screen, offset=(offset_x, offset_y))
        self.draw_ui()
