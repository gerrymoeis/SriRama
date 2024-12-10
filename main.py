import pygame
from mechanics.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE
from mechanics.game import Game
from core.ui import UI

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # font = pygame.font.Font("assets/fonts/main_font.ttf", 20)

    pygame.display.set_caption("SriRama: Dungeon Adventure")
    clock = pygame.time.Clock()

    game = Game(screen)
    ui = UI(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # Tombol Pause
                game.toggle_pause()
        
        screen.fill(WHITE)
        game.update()
        
        # Placeholder for UI
        # ui.draw_health_bar(10, 10, 200, 20, 80, 100)  # HP Bar
        # ui.draw_spiritual_bar(10, 40, 200, 20, 50, 100)  # Spiritual Bar
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()