import pygame

def draw_text(screen, text, x, y, font, color=(255, 255, 255), center=False):
    """Fungsi untuk menggambar teks di layar."""
    rendered_text = font.render(text, True, color)
    if center:
        x = x - rendered_text.get_width() // 2
        y = y - rendered_text.get_height() // 2
    screen.blit(rendered_text, (x, y))

class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.music_playing = False

    def play_music(self, music_path, loop=True):
        """
        Memutar musik. Menghindari pengulangan pemanggilan play jika musik sedang diputar.
        :param music_path: Path file musik.
        :param loop: True jika ingin looping musik.
        """
        if self.current_music != music_path or not self.music_playing:
            pygame.mixer.music.stop()  # Stop musik yang sedang diputar
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1 if loop else 0)
            self.current_music = music_path
            self.music_playing = True

    def stop_music(self):
        """Menghentikan musik."""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.current_music = None
            self.music_playing = False

    def is_music_playing(self):
        """Memeriksa apakah musik sedang diputar."""
        return pygame.mixer.music.get_busy()