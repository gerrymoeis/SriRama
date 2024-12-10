from game_objects.base import Entity

class Enemy(Entity):
    def __init__(self, x, y, width, height, color, speed, patrol_range):
        super().__init__(x, y, width, height, color)
        self.speed = speed
        self.patrol_range = patrol_range
        self.direction = 1  # 1 untuk maju, -1 untuk mundur
        self.start_x = x

    def patrol(self):
        self.rect.x += self.speed * self.direction
        if abs(self.rect.x - self.start_x) > self.patrol_range:
            self.direction *= -1  # Balik arah