import pygame
import sys
import os
import json
import random

pygame.init()

# --- Configuración general ---
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Tipo Deltarune Extendido")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont('Arial', 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ASSETS_DIR = "assets"
MAP_DIR = "map"
SAVE_DIR = "save"

# --- Funciones para cargar recursos ---
def load_image(name):
    path = os.path.join(ASSETS_DIR, name)
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        print(f"Error cargando imagen {name}: {e}")
        sys.exit()

def load_sound(name):
    path = os.path.join(ASSETS_DIR, name)
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"Error cargando sonido {name}: {e}")
        sys.exit()

def load_map():
    path = os.path.join(MAP_DIR, "map_data.json")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error cargando mapa: {e}")
        sys.exit()

# --- Sprites ---
player_sprites = {
    "idle": load_image("player_idle.png"),
    "walk": [load_image("player_walk1.png"), load_image("player_walk2.png")]
}

enemy_sprites = {
    "idle": load_image("enemy_idle.png"),
    "walk": [load_image("enemy_walk1.png"), load_image("enemy_walk2.png")]
}

# --- Sonidos y música ---
pygame.mixer.music.load(os.path.join(ASSETS_DIR, "bg_music.ogg"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

sound_select = load_sound("select.wav")
sound_confirm = load_sound("confirm.wav")
sound_attack = load_sound("confirm.wav")  # Reusa el mismo para ataque simple

# --- Variables globales ---
tile_size = 64
map_data = load_map()
game_map = map_data["map"]
tile_size = map_data["tile_size"]

# Posiciones iniciales
player_pos = [tile_size * 1, tile_size * 1]
player_speed = 4
player_frame = 0
player_frame_timer = 0

enemy_pos = [tile_size * 7, tile_size * 3]
enemy_speed = 2
enemy_frame = 0
enemy_frame_timer = 0

dialogue_active = False
battle_active = False
dialogue_index = 0
selected_option = 0
choices_made = []

# Variables batalla
player_hp = 30
enemy_hp = 20

# --- Funciones ---
def draw_text(text, x, y, color=WHITE):
    lines = text.split('\n')
    for i, line in enumerate(lines):
        rendered = FONT.render(line, True, color)
        screen.blit(rendered, (x, y + i*25))

def update_animation(moving, dt, frame_timer, frame, frames):
    if moving:
        frame_timer += dt
        if frame_timer > 200:
            frame = (frame + 1) % len(frames)
            frame_timer = 0
    else:
        frame = 0
        frame_timer = 0
    return frame_timer, frame

def can_move_to(pos):
    # Check colisiones en mapa (pos es [x,y] en píxeles)
    grid_x = int(pos[0] // tile_size)
    grid_y = int(pos[1] // tile_size)
    if grid_y < 0 or grid_y >= len(game_map):
        return False
    if grid_x < 0 or grid_x >= len(game_map[0]):
        return False
    return game_map[grid_y][grid_x] == 0

def move_enemy_towards_player(dt):
    global enemy_pos, enemy_frame, enemy_frame_timer

    direction = pygame.Vector2(player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1])
    if direction.length_squared() > 1:
        direction = direction.normalize()
        new_pos = [enemy_pos[0] + direction.x * enemy_speed, enemy_pos[1] + direction.y * enemy_speed]
        if can_move_to(new_pos):
            enemy_pos[0] = new_pos[0]
            enemy_pos[1] = new_pos[1]
        enemy_frame_timer, enemy_frame = update_animation(True, dt, enemy_frame_timer, enemy_frame, enemy_sprites["walk"])
    else:
        enemy_frame_timer, enemy_frame = update_animation(False, dt, enemy_frame_timer, enemy_frame, enemy_sprites["walk"])

def check_battle_start():
    # Si jugador y enemigo están muy cerca, empieza batalla
    dist = pygame.Vector2(player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]).length()
    return dist < 50

# --- Sistema diálogo simplificado ---
dialogues = [
    {"text": "Kael: ¿Dónde estoy?"},
    {"text": "Luma: Bienvenido al Reino de las Sombras.", "options": [
        {"text": "¿Quién eres?", "next": 2},
        {"text": "¿Qué está pasando?", "next": 3}
    ]},
    {"text": "Luma: Soy Luma, tu guía.", "next": 4},
    {"text": "Luma: El equilibrio está en peligro.", "next": 4},
    {"text": "Kael: ¿Qué debo hacer?", "options": [
        {"text": "Salvar el mundo", "next": 5, "choice": "save_world"},
        {"text": "¿Y si fallo?", "next": 6, "choice": "fail_doubt"}
    ]},
    {"text": "Luma: Debes ser valiente.", "next": 7},
    {"text": "Luma: El destino depende de ti.", "next": 7},
    {"text": "Kael: ¡Me prepararé para lo que venga!", "next": None}
]

def draw_dialogue(dialogue):
    pygame.draw.rect(screen, BLACK, (50, HEIGHT - 150, WIDTH - 100, 130))
    pygame.draw.rect(screen, WHITE, (50, HEIGHT - 150, WIDTH - 100, 130), 2)
    draw_text(dialogue["text"], 70, HEIGHT - 140)

    if "options" in dialogue:
        global selected_option
        for i, option in enumerate(dialogue["options"]):
            color = (255, 255, 0) if i == selected_option else WHITE
            draw_text(f"{i + 1}. {option['text']}", 70, HEIGHT - 100 + i * 30, color)

# --- Sistema batalla simple ---
battle_turn = "player"
battle_message = ""

def battle_player_attack():
    global enemy_hp, battle_message, battle_turn
    damage = random.randint(4, 8)
    enemy_hp -= damage
    battle_message = f"Atacaste al enemigo por {damage} puntos."
    battle_turn = "enemy"

def battle_enemy_attack():
    global player_hp, battle_message, battle_turn
    damage = random.randint(3, 7)
    player_hp -= damage
    battle_message = f"El enemigo te atacó por {damage} puntos."
    battle_turn = "player"

def draw_battle():
    screen.fill((50, 0, 0))
    draw_text(f"Batalla - Tu HP: {player_hp}", 20, 20)
    draw_text(f"Enemigo HP: {enemy_hp}", 20, 50)
    draw_text(battle_message, 20, 90)
    draw_text("Presiona A para atacar, Q para rendirte", 20, HEIGHT - 40)

def save_game():
    save_data = {
        "player_pos": player_pos,
        "player_hp": player_hp,
        "enemy_pos": enemy_pos,
        "enemy_hp": enemy_hp,
        "choices": choices_made
    }
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    with open(os.path.join(SAVE_DIR, "savegame.json"), "w") as f:
        json.dump(save_data, f)

def load_game():
    global player_pos, player_hp, enemy_pos, enemy_hp, choices_made
    path = os.path.join(SAVE_DIR, "savegame.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            player_pos = data.get("player_pos", player_pos)
            player_hp = data.get("player_hp", player_hp)
            enemy_pos = data.get("enemy_pos", enemy_pos)
            enemy_hp = data.get("enemy_hp", enemy_hp)
            choices_made = data.get("choices", [])

def show_final_screen(choice):
    screen.fill(BLACK)
    if choice == "save_world":
        text = "¡Has salvado ambos mundos! Final bueno."
    elif choice == "fail_doubt":
        text = "Has dudado y la oscuridad triunfó. Final malo."
    else:
        text = "Final neutral. Aún hay esperanza."
    draw_text(text, WIDTH//2 - 150, HEIGHT//2 - 10, WHITE)
    pygame.display.flip()
    pygame.time.wait(5000)  # muestra 5 segundos

# --- Loop principal ---
def main():
    global dialogue_active, dialogue_index, selected_option, choices_made
    global player_frame, player_frame_timer, enemy_frame, enemy_frame_timer
    global battle_active, battle_turn, battle_message
    global player_hp, enemy_hp

    running = True
    dialogue_active = True
    battle_active = False

    player_moving = False
    player_dir = pygame.Vector2(0, 0)

    load_game()

    while running:
        dt = clock.tick(60)
        screen.fill((30, 30, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                running = False

            if dialogue_active:
                if event.type == pygame.KEYDOWN:
                    dialogue = dialogues[dialogue_index]

                    if "options" in dialogue:
                        if event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % len(dialogue["options"])
                            sound_select.play()
                        elif event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % len(dialogue["options"])
                            sound_select.play()
                        elif event.key == pygame.K_RETURN:
                            choice = dialogue["options"][selected_option].get("choice", None)
                            if choice:
                                choices_made.append(choice)
                            next_index = dialogue["options"][selected_option]["next"]
                            sound_confirm.play()
                            if next_index is not None:
                                dialogue_index = next_index
                                selected_option = 0
                            else:
                                dialogue_active = False
                    else:
                        if event.key == pygame.K_RETURN:
                            choice = dialogue.get("choice", None)
                            if choice:
                                choices_made.append(choice)
                            sound_confirm.play()
                            if "next" in dialogue and dialogue["next"] is not None:
                                dialogue_index = dialogue["next"]
                            else:
                                dialogue_active = False

            elif battle_active:
                if event.type == pygame.KEYDOWN:
                    if battle_turn == "player":
                        if event.key == pygame.K_a:
                            battle_player_attack()
                            sound_attack.play()
                            if enemy_hp <= 0:
                                battle_message = "¡Ganaste la batalla!"
                                battle_active = False
                                # Puedes añadir lógica de recompensa aquí
                        elif event.key == pygame.K_q:
                            battle_message = "¡Huiste de la batalla!"
                            battle_active = False
                    elif battle_turn == "enemy":
                        # Espera un poco o responde automáticamente después del turno enemigo
                        pass

            else:
                keys = pygame.key.get_pressed()
                player_dir = pygame.Vector2(0, 0)
                if keys[pygame.K_LEFT]:
                    player_dir.x = -1
                if keys[pygame.K_RIGHT]:
                    player_dir.x = 1
                if keys[pygame.K_UP]:
                    player_dir.y = -1
                if keys[pygame.K_DOWN]:
                    player_dir.y = 1

                player_moving = player_dir.length_squared() > 0
                if player_moving:
                    player_dir = player_dir.normalize()
                    new_pos = [player_pos[0] + player_dir.x * player_speed, player_pos[1] + player_dir.y * player_speed]
                    if can_move_to(new_pos):
                        player_pos[0] = new_pos[0]
                        player_pos[1] = new_pos[1]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        dialogue_active = True
                        dialogue_index = 0
                        selected_option = 0
                        choices_made = []
                    if event.key == pygame.K_s:
                        save_game()
                    if event.key == pygame.K_l:
                        load_game()

        # Actualizar animaciones jugador y enemigo
        player_frame_timer, player_frame = update_animation(player_moving, dt, player_frame_timer, player_frame, player_sprites["walk"])
        move_enemy_towards_player(dt)

        # Detectar inicio de batalla
        if not dialogue_active and not battle_active and check_battle_start():
            battle_active = True
            battle_turn = "player"
            battle_message = "¡Comienza la batalla!"

        # Dibujar según estado
        if dialogue_active:
            draw_dialogue(dialogues[dialogue_index])
        elif battle_active:
            draw_battle()
            if battle_turn == "enemy" and battle_active:
                # Turno enemigo automático después de retraso simple
                pygame.time.wait(500)
                battle_enemy_attack()
                if player_hp <= 0:
                    battle_message = "Has sido derrotado..."
                    battle_active = False
                battle_turn = "player"
        else:
            # Dibujar mapa simple
            for y, row in enumerate(game_map):
                for x, tile in enumerate(row):
                    color = (100, 100, 100) if tile == 1 else (50, 50, 100)
                    pygame.draw.rect(screen, color, (x*tile_size, y*tile_size, tile_size, tile_size))

            # Dibujar jugador y enemigo
            if player_moving:
                current_player_sprite = player_sprites["walk"][player_frame]
            else:
                current_player_sprite = player_sprites["idle"]
            screen.blit(current_player_sprite, player_pos)

            current_enemy_sprite = enemy_sprites["walk"][enemy_frame] if enemy_frame != 0 else enemy_sprites["idle"]
            screen.blit(current_enemy_sprite, enemy_pos)

            draw_text("Flechas para mover, ESPACIO para diálogo", 10, 10)
            draw_text("S para guardar, L para cargar", 10, 40)

            # Si ya hay elecciones, mostrar final simple y terminar
            if choices_made:
                show_final_screen(choices_made[0])
                running = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
      
