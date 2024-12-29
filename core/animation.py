import pygame

class Animation:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, frame_count, frame_rate, scales):
        """
        Mengelola animasi dari sprite sheet.
        :param sprite_sheet_path: Path ke file sprite sheet.
        :param frame_width: Lebar tiap frame.
        :param frame_height: Tinggi tiap frame.
        :param frame_count: Jumlah frame dalam animasi.
        :param frame_rate: Kecepatan animasi (frame per detik).
        :param scales: Mengatur ukuran sprite asset gambar
        """
        self.scales = scales

        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_count = frame_count
        self.frame_rate = frame_rate
        self.frames = self._extract_frames()
        self.current_frame_index = 0
        self.time_since_last_frame = 0


    def _extract_frames(self):
        """Ekstraksi frame dari sprite sheet ke dalam daftar."""
        frames = []
        sheet_width = self.sprite_sheet.get_width()
        for i in range(self.frame_count):
            x = (i * self.frame_width) % sheet_width
            y = (i * self.frame_width) // sheet_width * self.frame_height
            
            frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
            frame.blit(self.sprite_sheet, (0, 0), (0, 0, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (48 * self.scales, 64 * self.scales))
            
            frames.append(frame)
        return frames

    def get_current_frame(self):
        """Mengembalikan frame animasi saat ini."""
        return self.frames[self.current_frame_index]

    def update(self, dt):
        """
        Memperbarui frame animasi berdasarkan waktu yang berlalu.
        :param dt: Delta time sejak frame terakhir.
        """
        self.time_since_last_frame += dt
        if self.time_since_last_frame > 1000 / self.frame_rate:
            self.current_frame_index = (self.current_frame_index + 1) % self.frame_count
            self.time_since_last_frame = 0
