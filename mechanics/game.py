import pygame
import random

from mechanics.config import SCREEN_WIDTH, SCREEN_HEIGHT, RED, BLUE, GREEN

from game_objects.characters import Sri, Rama
from game_objects.enemies import EnemyRandom
from game_objects.coin import Coin

from core.animation import Animation

from core.ui import UI, PauseMenu, GameOver, SkillCooldownUI

class Game:
    def __init__(self, screen, asset_manager):
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
        
        self.sri_ui = SkillCooldownUI(self.screen, self.players[0], BLUE, (SCREEN_WIDTH - 300, 50))
        self.rama_ui = SkillCooldownUI(self.screen, self.players[1], RED, (SCREEN_WIDTH - 300, 100))

        self.font = pygame.font.Font(None, 36)
        self.start_time = 0  # Waktu mulai stopwatch
        self.elapsed_time = 0  # Waktu bertahan pemain

        self.coin_timer = 0
        self.coins = []  # Daftar koin
        self.score = 0  # Skor pemain
        self.coin_spawn_interval = 3000  # Interval spawn koin dalam milidetik (3 detik)

        self.enemies_animations = [
            {"idle": Animation("assets/images/monsters/normal/16x16/bat.png", 16, 16, 3, 5, 1.25)},
            {"idle": Animation("assets/images/monsters/normal/16x16/skeleton.png", 16, 16, 3, 5, 1.25)},
            {"idle": Animation("assets/images/monsters/normal/16x16/rat.png", 16, 16, 2, 5, 1.25)},
            {"idle": Animation("assets/images/monsters/normal/16x16/spider.png", 16, 16, 2, 5, 1.25)},
            {"idle": Animation("assets/images/monsters/normal/16x16/ghost.png", 16, 16, 3, 5, 1.25)},
        ]

        self.asset_manager = asset_manager
        self.background = self.asset_manager.get_image("gameplay_bg")
        
        self.reset_game()

    def reset_game(self):
        """Reset state game dengan randomisasi untuk posisi, jumlah enemy, dan atribut lainnya."""
        self.players = [
            Sri(100, 100, 40, 40, 5, self.screen),
            Rama(200, 100, 40, 40, 5, self.screen)
        ]
        
        self.sri_ui = SkillCooldownUI(self.screen, self.players[0], BLUE, (SCREEN_WIDTH - 300, 50))
        self.rama_ui = SkillCooldownUI(self.screen, self.players[1], RED, (SCREEN_WIDTH - 300, 100))

        # Randomisasi jumlah musuh antara 3-6
        num_enemies = random.randint(3, 6)
        self.enemies = [
            EnemyRandom(
                random.randint(0, SCREEN_WIDTH - 50),
                random.randint(-50, -25),
                40, 40,
                (0, random.randint(100, 255), 0),  # Hijau acak untuk warna
                random.randint(1, 2),  # Kecepatan acak
                random.randint(50, 150),  # Jarak Patrol
                self.enemies_animations[random.randint(0, 4)]
            ) for _ in range(num_enemies)
        ]

        self.hp = self.max_hp
        self.spiritual_bar = 50
        self.all_sprites = self.enemies
        self.shake_intensity = 0
        self.damage_cooldown = 0

        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0

        self.coin_timer = 0
        self.coins = []
        self.score = 0
        self.coin_spawn_interval = 3000  # Reset interval spawn koin

        self.clock = pygame.time.Clock()

        self.unpause_game()

    def prevent_player_out_of_bounds(self):
        """Mencegah player keluar dari layar."""
        for player in self.players:
            if player.image_rect.left < 0:
                player.image_rect.left = 0
            if player.image_rect.right > SCREEN_WIDTH:
                player.image_rect.right = SCREEN_WIDTH
            if player.image_rect.top < 0:
                player.image_rect.top = 0
            if player.image_rect.bottom > SCREEN_HEIGHT:
                player.image_rect.bottom = SCREEN_HEIGHT
    
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
                    random.randint(1, 2),  # Kecepatan acak
                    random.randint(50, 150), # Jarak Patrol
                    self.enemies_animations[random.randint(0, 4)])
                
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
                if player.image_rect.colliderect(enemy.image_rect) and self.damage_cooldown == 0 and not player.invisible:
                    self.hp -= 5
                    player.color = (0, 0, 0)
                    self.shake_intensity = 20
                    self.damage_cooldown = 10

                    self.draw()

    def check_game_over(self):
        if self.hp <= 0:
            return "LOSE"
        if not self.enemies:
            return "WIN"
        return None

    def draw_ui(self):
        self.ui.draw_health_bar(10, 10, 500, 20, self.hp, self.max_hp)

        [sri, rama] = self.players
        self.sri_ui.draw("Sri", sri.skill_cooldown)
        self.rama_ui.draw("Rama", rama.skill_cooldown)

        # Tampilkan stopwatch
        stopwatch_text = self.font.render(f"Time Survived: {self.elapsed_time}s", True, (255, 255, 255))
        self.screen.blit(stopwatch_text, (SCREEN_WIDTH // 2 - stopwatch_text.get_width() // 2, 25))

        # Tampilkan skor
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 0))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 75))

    def apply_shake_effect(self):
        if self.shake_intensity > 0:
            offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity = max(self.shake_intensity - 1, 0)
            return offset_x, offset_y
        return 0, 0
    
    def spawn_coins(self):
        """Spawn koin secara random."""
        num_coins = random.randint(1, 3)  # Jumlah koin dalam satu cycle
        for _ in range(num_coins):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(50, SCREEN_HEIGHT - 50)
            self.coins.append(Coin(x, y))

    def update(self):
        dt = self.clock.tick(60)  # Delta time (ms)
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
                    self.game_over.draw(self.elapsed_time, self.score)
                self.last_input_time = current_time  # Reset cooldown
            elif game_state == "WIN":
                self.ui.draw_message("YOU WIN!", GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                return
            else:
                self.screen.blit(self.background, (SCREEN_WIDTH // 2 - self.background.get_width() // 2, SCREEN_HEIGHT // 2 - self.background.get_height() // 2))

                self.elapsed_time = (current_time - self.start_time) // 1000  # Dalam detik

                self.handle_input()
                self.prevent_player_out_of_bounds()
                self.check_collisions()
                
                self.spawn_enemy()

                for enemy in self.enemies:
                    enemy.chase(self.players)
                    enemy.draw(self.screen)

                for player in self.players:
                    player.draw(self.screen)
                    player.update(dt)

                    player.color = player.default_color
                    player.update_skill(current_time)
                
                # Handle input untuk skill
                [sri, rama] = self.players
                keys = pygame.key.get_pressed()
                if keys[pygame.K_f]:  # Aktivasi skill untuk Sri
                    sri.activate_skill()
                if keys[pygame.K_RSHIFT]:  # Aktivasi skill untuk Rama
                    rama.activate_skill()
                
                if sri.skill_active:
                    sri.create_dash_area()  # Tampilkan area dash selama skill aktif
                if rama.skill_active:
                    rama.create_healing_area(self.enemies)  # Tampilkan area healing selama skill aktif
                    self.hp += 0.25
                
                if self.hp >= self.max_hp:
                    self.hp = self.max_hp

                # Input untuk Sri
                if keys[pygame.K_w] or keys[pygame.K_a] or keys[pygame.K_s] or keys[pygame.K_d]:
                    sri.set_animation("walk")
                else:
                    sri.set_animation("idle")

                # Input untuk Rama
                if keys[pygame.K_UP] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or keys[pygame.K_RIGHT]:
                    rama.set_animation("walk")
                else:
                    rama.set_animation("idle")
                
                # Spawn koin
                if current_time - self.coin_timer > self.coin_spawn_interval:
                    self.coin_timer = current_time
                    self.spawn_coins()

                # Update koin
                for coin in self.coins[:]:
                    if coin.collides_with(sri.image_rect) or coin.collides_with(rama.image_rect):
                        self.coins.remove(coin)
                        self.score += 1  # Tambahkan skor
                        self.coin_spawn_interval = max(500, self.coin_spawn_interval - 50)  # Akselerasi spawn

                for coin in self.coins:
                    coin.draw(self.screen)
                
                self.draw_ui()

    def draw(self):
        offset_x, offset_y = self.apply_shake_effect()
        for sprite in self.all_sprites:
            sprite.draw(self.screen, offset=(offset_x, offset_y))
            # sprite.update(dt, self.screen)

        for player in self.players:
            player.draw(self.screen, offset=(offset_x, offset_y))

        self.draw_ui()
