import pygame
from src.player import Player
from src.enemy import Enemy
from src.battle import Battle
from src.dialogue import Dialogue
from src.story import Story
from src.music_manager import MusicManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Deltarune RPG")
    clock = pygame.time.Clock()

    # Crear instancias
    player = Player("Héroe", 100)
    enemy = Enemy("Goblin", 50)
    battle = Battle(player, enemy)
    music_manager = MusicManager()
    story = Story()

    # Reproducir música de fondo
    music_manager.play_music("assets/audio/fondo_batalla.mp3")

    # Lógica del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Aquí iría la lógica del juego: diálogos, combate, etc.

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

