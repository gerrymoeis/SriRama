import pygame

def process_controls(keys, player1, player2):
    # Kontrol untuk Player 1 (WASD)
    player1.move(keys, up=pygame.K_w, down=pygame.K_s, left=pygame.K_a, right=pygame.K_d)
    # Kontrol untuk Player 2 (Arrow Keys)
    player2.move(keys, up=pygame.K_UP, down=pygame.K_DOWN, left=pygame.K_LEFT, right=pygame.K_RIGHT)