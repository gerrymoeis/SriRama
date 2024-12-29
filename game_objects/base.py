import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, animations, current_animation="idle"):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

        self.x = x
        self.y = y
        self.animations = animations
        self.current_animation = current_animation
        self.image = self.animations[self.current_animation].get_current_frame()

        self.image_for_rect = pygame.transform.scale(self.image, (64, 81))
        self.image_rect = self.image_for_rect.get_rect(topleft=(500, 500))

        self.velocity = pygame.Vector2(0, 0)

    def draw_placeholder(self, screen, offset=(0, 0)):
        self.rect.x += offset[0]
        self.rect.y += offset[1]
        pygame.draw.rect(screen, self.color, self.rect)
    
    def draw(self, screen, offset=(0, 0)):
        """Menggambar sprite ke layar."""
        self.image_rect.x += offset[0]
        self.image_rect.y += offset[1]
        screen.blit(self.image, (self.image_rect.x - 64 // 1.5, self.image_rect.y - 81 // 1.5))
    
    def set_animation(self, animation_name):
        """Mengatur animasi berdasarkan nama."""
        if animation_name in self.animations and self.current_animation != animation_name:
            self.current_animation = animation_name
    
    def update(self, dt):
        """Memperbarui animasi dan posisi karakter."""
        self.animations[self.current_animation].update(dt)
        self.image = self.animations[self.current_animation].get_current_frame()
        self.image_rect.topleft += self.velocity * dt
