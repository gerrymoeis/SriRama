from game_objects.base import Entity

class Character(Entity):
    def __init__(self, x, y, width, height, color, speed):
        super().__init__(x, y, width, height, color)
        self.speed = speed

    def move(self, keys, up, down, left, right):
        if keys[up]:
            self.rect.y -= self.speed
        if keys[down]:
            self.rect.y += self.speed
        if keys[left]:
            self.rect.x -= self.speed
        if keys[right]:
            self.rect.x += self.speed