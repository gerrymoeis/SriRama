import pygame

class AssetManager:
    def __init__(self):
        self.images = {}
        self.music = {}
        self.sfx = {}

        self.current_music = None
        self.music_playing = False

    def load_image(self, name, path):
        """Memuat gambar dari path dan menyimpannya dengan nama unik."""
        try:
            image = pygame.image.load(path).convert_alpha()
            self.images[name] = image
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")

    def get_image(self, name):
        """Mengambil gambar berdasarkan nama."""
        return self.images.get(name)

    def load_music(self, name, path):
        """Memuat musik BGM."""
        try:
            self.music[name] = path
        except pygame.error as e:
            print(f"Error loading music {path}: {e}")

    def play_music(self, name, loops=-1):
        """
        Memutar musik. Menghindari pengulangan pemanggilan play jika musik sedang diputar.
        :param music_path: Path file musik.
        :param loop: True jika ingin looping musik.
        """

        path = self.music.get(name)

        if self.current_music != path or not self.music_playing:
            pygame.mixer.music.stop()  # Stop musik yang sedang diputar
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(loops)
            self.current_music = path
            self.music_playing = True
 
    def stop_music(self):
        """Menghentikan musik yang sedang dimainkan."""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.current_music = None
            self.music_playing = False

    def load_sfx(self, name, path):
        """Memuat efek suara (SFX)."""
        try:
            sound = pygame.mixer.Sound(path)
            self.sfx[name] = sound
        except pygame.error as e:
            print(f"Error loading SFX {path}: {e}")

    def play_sfx(self, name):
        """Memainkan efek suara berdasarkan nama."""
        sound = self.sfx.get(name)
        if sound:
            sound.play()
        else:
            print(f"SFX {name} not found!")
