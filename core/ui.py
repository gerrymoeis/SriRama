import pygame
from mechanics.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, RED

from src.utils import draw_text

class UI:
    def __init__(self, screen, size=25):
        self.screen = screen
        self.size = size
        self.font = pygame.font.Font("assets/fonts/main_font.ttf", self.size)

    def draw_health_bar(self, x, y, width, height, current_hp, max_hp):
        # Hitung panjang bar berdasarkan HP
        hp_percentage = current_hp / max_hp
        bar_width = int(width * hp_percentage)

        # Bar background
        pygame.draw.rect(self.screen, (100, 100, 100), (x, y, width, height))
        # Bar foreground
        pygame.draw.rect(self.screen, RED, (x, y, bar_width, height))
        # Border
        pygame.draw.rect(self.screen, BLACK, (x, y, width, height), 2)

class StartMenu(UI):
    def __init__(self, screen, asset_manager):
        super().__init__(screen)

        self.options = ["Start Game", "Settings", "Exit Game"]
        self.selected_option = 0
        self.last_input_time = 0  # Timer untuk mengontrol input
        self.input_cooldown = 200  # Cooldown dalam milidetik (0.2 detik)

        self.asset_manager = asset_manager
        self.background = self.asset_manager.get_image("start_menu_bg")

    def draw(self):
        self.screen.blit(self.background, (SCREEN_WIDTH // 2 - self.background.get_width() // 2, SCREEN_HEIGHT // 2 - self.background.get_height() // 2))

        self.font = pygame.font.Font("assets/fonts/main_font.ttf", 40)
        draw_text(self.screen, "SriRama: Dungeon Survivor", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.font, color=(255, 255, 255), center=True)

        self.font = pygame.font.Font("assets/fonts/main_font.ttf", self.size)
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            draw_text(self.screen, option, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 50 + 100, self.font, color=color, center=True)

    def handle_input(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_input_time < self.input_cooldown:
            return None  # Abaikan input jika masih dalam cooldown
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.last_input_time = current_time  # Reset timer
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.last_input_time = current_time  # Reset timer
        elif keys[pygame.K_RETURN]:
            return self.options[self.selected_option]
        return None

class SettingMenu(UI):
    def __init__(self, screen):
        super().__init__(screen)

        self.options = ["Volume: 50", "Resolution: 800x600", "Back"]
        self.selected_option = 0
        self.volume = 50
        self.resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
        self.current_resolution_index = 0
        self.text = "Setting"
        self.last_input_time = 0  # Timer untuk mengontrol input
        self.input_cooldown = 200  # Cooldown dalam milidetik (0.2 detik)

    def draw(self):
        self.screen.fill((30, 30, 30))  # Background color
        title = self.font.render(self.text, True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - title.get_height() // 2 - 150))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (150, 150, 150)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, (SCREEN_HEIGHT // 2 - title.get_height() // 2) + i * 70))

    def update_resolution(self, current_resolution_index):
        self.current_resolution_index = current_resolution_index
        resolution = self.resolutions[self.current_resolution_index]
        self.options[1] = f"Resolution: {resolution[0]}x{resolution[1]}"
    
    def handle_input(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_input_time < self.input_cooldown:
            return None  # Abaikan input jika masih dalam cooldown
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.last_input_time = current_time  # Reset timer
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.last_input_time = current_time  # Reset timer
        elif keys[pygame.K_RETURN]:
            if self.selected_option == 0:  # Adjust volume
                self.volume = (self.volume + 10) % 110
                self.options[0] = f"Volume: {self.volume}"
                self.last_input_time = current_time  # Reset timer                
            elif self.selected_option == 1:  # Change resolution
                self.current_resolution_index = (self.current_resolution_index + 1) % len(self.resolutions)
                resolution = self.resolutions[self.current_resolution_index]
                self.options[1] = f"Resolution: {resolution[0]}x{resolution[1]}"
                self.last_input_time = current_time  # Reset timer
            elif self.selected_option == 2:  # Back
                return "Start Menu"
        return None

class PauseMenu(SettingMenu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = ["Volume: 50", "Resolution: 800x600", "Back", "Start Menu"]
        self.text = "Paused"
        
    def update_resolution(self, current_resolution_index):
        self.current_resolution_index = current_resolution_index
        resolution = self.resolutions[self.current_resolution_index]
        self.options[1] = f"Resolution: {resolution[0]}x{resolution[1]}"

    def handle_input(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_input_time < self.input_cooldown:
            return None  # Abaikan input jika masih dalam cooldown
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.last_input_time = current_time  # Reset timer
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.last_input_time = current_time  # Reset timer
        elif keys[pygame.K_RETURN]:
            if self.selected_option == 0:  # Adjust volume
                self.volume = (self.volume + 10) % 110
                self.options[0] = f"Volume: {self.volume}"
                self.last_input_time = current_time  # Reset timer
            elif self.selected_option == 1:  # Change resolution
                self.current_resolution_index = (self.current_resolution_index + 1) % len(self.resolutions)
                resolution = self.resolutions[self.current_resolution_index]
                self.options[1] = f"Resolution: {resolution[0]}x{resolution[1]}"
                self.last_input_time = current_time  # Reset timer
            elif self.selected_option == 2:  # Back
                return "Back"
            elif self.selected_option == 3:  # Start Menu
                return "Start Menu"
        return None
    
class GameOver(SettingMenu):
    def __init__(self, screen):
        super().__init__(screen)
        self.options = ["Retry", "Back to Start Menu"]
        self.text = "GAME OVER"

    def draw(self, elapsed_time, score):
        super().draw()

        # Tampilkan waktu bertahan
        survived_text = self.font.render(f"Time Survived: {elapsed_time}s", True, (255, 255, 255))
        self.screen.blit(survived_text, (SCREEN_WIDTH // 2 - survived_text.get_width() // 2, 200))

        # Tampilkan skor
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 0))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 250))
    
    def handle_input(self):
        """Mengontrol navigasi dan pemilihan menu."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_input_time < self.input_cooldown:
            return None  # Abaikan input jika masih dalam cooldown

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
            self.last_input_time = current_time
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
            self.last_input_time = current_time
        elif keys[pygame.K_RETURN]:
            # Mengembalikan pilihan yang dipilih
            return self.options[self.selected_option]
        return None

class SkillCooldownUI(UI):
    def __init__(self, screen, character, color, position):
        super().__init__(screen, size=20)
        
        self.character = character
        self.color = color
        self.position = position

    def draw(self, name, skill_cooldown):
        cooldown_text = f"{name} Skill: {max(skill_cooldown // 1000, 0)}s"
        text_surface = self.font.render(cooldown_text, True, self.color)
        self.screen.blit(text_surface, self.position)
