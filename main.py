import pygame
from mechanics.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE
from mechanics.game import Game
from core.ui import StartMenu, SettingMenu

from src.assets_manager import AssetManager
from src.utils import AudioManager

class MainGame:
    def __init__(self, current_state="start_menu"):
        self.resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
        self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)

        pygame.init()
        self.screen = pygame.display.set_mode(self.resolution, pygame.RESIZABLE)
        pygame.display.set_caption("SriRama: Dungeon Survivor")
                
        self.clock = pygame.time.Clock()
        self.last_input_time = 0
        self.input_cooldown = 200

        self.asset_manager = AssetManager()
        self.audio_manager = AudioManager()
        self.load()
        
        self.start_menu = StartMenu(self.screen, self.asset_manager)
        self.game = Game(self.screen, self.asset_manager)
        self.settings_menu = SettingMenu(self.screen)
        self.current_state = current_state
        self.running = True
            
    def load(self):
        self.asset_manager.load_image("start_menu_bg", "assets/images/backgrounds/UI-Menu Background.jpg")
        self.asset_manager.load_image("gameplay_bg", "assets/images/backgrounds/gameplay_bg.png")
        self.asset_manager.load_music("start_menu_bgm", "assets/sounds/bgm/In Pursuit of Freedom Loop.mp3")
        self.asset_manager.load_music("gameplay_bgm", "assets/sounds/bgm/In Freedom to Critical Clash 2.mp3")
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            current_time = pygame.time.get_ticks()

            if self.current_state == "start_menu":
                self.asset_manager.play_music("start_menu_bgm")

                self.start_menu.draw()
                if current_time - self.last_input_time > self.input_cooldown:
                    selected_option = self.start_menu.handle_input()
                    if selected_option == "Start Game":
                        self.current_state = "gameplay"
                    elif selected_option == "Settings":
                        self.current_state = "settings"
                    elif selected_option == "Exit Game":
                        self.running = False
                    if selected_option:
                        self.last_input_time = current_time  # Reset cooldown

            elif self.current_state == "settings":
                self.settings_menu.draw()
                
                if current_time - self.last_input_time > self.input_cooldown:
                    selected_option = self.settings_menu.handle_input()
                    self.resolution = self.resolutions[self.settings_menu.current_resolution_index]
                    
                    if selected_option == "Start Menu":
                        self.current_state = "start_menu"
                    if selected_option:
                        self.last_input_time = current_time  # Reset cooldown

            elif self.current_state == "gameplay":
                self.asset_manager.play_music("gameplay_bgm")

                self.screen.fill(WHITE)
                self.game.update()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.game.pause_game()

                elif current_time - self.last_input_time > self.input_cooldown and self.game.paused:
                    selected_option = self.game.pause_menu.handle_input()
                    self.resolution = self.resolutions[self.game.pause_menu.current_resolution_index]

                    if selected_option == "Back":
                        self.game.unpause_game()
                    elif selected_option == "Start Menu":
                        self.current_state = "start_menu"
                        self.game.reset_game()
                    if selected_option:
                        self.last_input_time = current_time  # Reset cooldown
                
                elif self.game.check_game_over() == "LOSE":
                    selected_option = self.game.game_over.handle_input()

                    if selected_option == "Retry":
                        self.game.reset_game()
                    elif selected_option == "Back to Start Menu":
                        self.current_state = "start_menu"
                        self.game.reset_game()
                    if selected_option:
                        self.last_input_time = current_time  # Reset cooldown

            pygame.display.flip()
            self.clock.tick(FPS)

        self.asset_manager.stop_music()
        pygame.quit()

if __name__ == "__main__":
    game = MainGame()
    game.run()
