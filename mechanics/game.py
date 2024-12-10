import pygame
from mechanics.config import SCREEN_WIDTH, SCREEN_HEIGHT, RED, BLUE, GREEN
from game_objects.characters import Character
from game_objects.enemies import Enemy
from core.ui import UI, PauseMenu

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player1 = Character(100, 100, 40, 40, RED, 5)  # Player 1
        self.player2 = Character(200, 100, 40, 40, BLUE, 5)  # Player 2
        self.max_hp = 100
        self.hp = self.max_hp

        self.enemy = Enemy(400, 300, 40, 40, (0, 255, 0), 2, 100)  # Musuh dengan patrol
        self.all_sprites = [self.player1, self.player2, self.enemy]
        self.pause_menu = PauseMenu(screen)
        self.paused = False

        self.ui = UI(screen)
        self.spiritual_bar = 50  # Nilai awal
        self.max_spiritual_bar = 100
    
    def toggle_pause(self):
        self.paused = not self.paused

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Kontrol Player 1 (WASD)
        self.player1.move(keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        # Kontrol Player 2 (Arrow Keys)
        self.player2.move(keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
    
    def check_collisions(self):
        if self.player1.rect.colliderect(self.enemy.rect):
            self.hp -= 1  # Kurangi HP
            self.player1.color = (255, 200, 200)  # Efek warna saat terkena damage
        if self.player2.rect.colliderect(self.enemy.rect):
            self.hp -= 1
            self.player2.color = (200, 200, 255)
    
    def check_game_over(self):
        if self.hp <= 0 or self.hp <= 0:
            return "LOSE"
        # Placeholder untuk win condition, bisa diubah nanti
        if self.enemy is None:  
            return "WIN"
        return None
    
    def handle_spiritual_mechanics(self):
        # Contoh sederhana: mengisi spiritual bar saat tombol ditekan
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.spiritual_bar = min(self.max_spiritual_bar, self.spiritual_bar + 1)

    def draw_ui(self):
        self.ui.draw_health_bar(10, 10, 200, 20, self.hp, self.max_hp)
        self.ui.draw_spiritual_bar(10, 40, 200, 20, self.spiritual_bar, self.max_spiritual_bar)

    def update(self):
        if self.paused:
            self.pause_menu.draw()
        else:
            self.handle_input()
            self.enemy.patrol()
            self.check_collisions()  # Panggil fungsi collision
            self.handle_spiritual_mechanics()  # Mekanisme spiritual

            # Reset warna player jika tidak terkena damage
            self.player1.color = RED
            self.player2.color = BLUE

            # Cek kondisi game
            game_state = self.check_game_over()
            if game_state == "LOSE":
                self.ui.draw_message("YOU LOSE!", RED, 300, 250)
                return
            elif game_state == "WIN":
                self.ui.draw_message("YOU WIN!", GREEN, 300, 250)
                return
            
            self.draw_ui()  # Tambahkan UI

            for sprite in self.all_sprites:
                sprite.draw(self.screen)