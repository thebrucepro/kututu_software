# main.py
import pygame
from player import Player
from enemy import Enemy
from battle import Battle
from dialogue import Dialogue
from story import Story
from music_manager import MusicManager

def main():
    # Inicializar pygame
    pygame.init()

    # Crear instancias de música, jugador, enemigo y batalla
    music_manager = MusicManager()
    player = Player("Héroe", 100)
    enemy = Enemy("Goblin", 50)
    battle = Battle(player, enemy)
    historia = Story()

    # Reproducir música de fondo
    music_manager.play_music("fondo_aventura.mp3")

    # Mostrar un diálogo de introducción
    dialogo = Dialogue("Te encuentras en un bosque oscuro. ¿Qué haces?", ["Explorar", "Descansar"])
    eleccion = dialogo.display()
    historia.update_flags(eleccion)

    # Iniciar el combate
    resultado = battle.battle()

    # Mostrar el resultado del combate
    if resultado == "victoria":
        print("¡Has ganado el combate!")
    elif resultado == "derrota":
        print
::contentReference[oaicite:0]{index=0}

