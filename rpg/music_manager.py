import pygame

class MusicManager:
    def __init__(self):
        pygame.mixer.init()
        self.volume = 0.1  # Volumen predeterminado

    def play_music(self, track, loop=-1):
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(loop, 0.0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sound(self, sound):
        sound.play()
      
