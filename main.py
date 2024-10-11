from hero import Hero
from enemy import Enemy
import pgzrun
import random
import pygame

# Dimensões do mapa (16x16 tiles, cada um com 16x16 pixels)
WIDTH = 256
HEIGHT = 256
TILE_SIZE = 16

# Estados do jogo
MENU, PLAYING, VICTORY, DEFEAT = 'menu', 'playing', 'victory', 'defeat'
game_state = MENU

# Música e sons
sound_on = True
sounds.background.play(True)

# Mapa: 0 = chão, 1 = parede
map_layout = [[0 if random.random() > 0.2 else 1 for _ in range(16)] for _ in range(16)]

# Posição aleatória válida no mapa
def get_random_position():
    while True:
        x, y = random.randint(0, 15) * TILE_SIZE, random.randint(0, 15) * TILE_SIZE
        col, row = x // TILE_SIZE, y // TILE_SIZE
        if map_layout[row][col] == 0:
            return (x+8, y+8)

# Som de vitória
def play_victory_sound():
    if sound_on:
        sounds.victory.play()

# Som de derrota
def play_defeat_sound():
    if sound_on:
        sounds.defeat.play()

# Verifica se o mouse está sobre o texto
def is_text_hovered(text_pos, text_width, text_height, mouse_pos):
    x, y = text_pos
    return x < mouse_pos[0] < x + text_width and y < mouse_pos[1] < y + text_height

# Desenha o menu
def draw_menu():
    screen.clear()
    title_pos = (16, 16)
    subtitle_pos = (16, 52)
    menu_instrc_pos = (16, 100)
    start_pos = (16, HEIGHT // 2)
    music_pos = (16, HEIGHT // 2 + 32)
    exit_pos = (16, HEIGHT // 2 + 64)
    mouse_pos = pygame.mouse.get_pos()

    # Destaca o botão com fundo cinza se o mouse passar por cima
    if is_text_hovered(start_pos, 180, 30, mouse_pos):
        screen.draw.filled_rect(Rect(start_pos[0] - 5, start_pos[1], 180, 30), (100, 100, 100))
    if is_text_hovered(music_pos, 180, 30, mouse_pos):
        screen.draw.filled_rect(Rect(music_pos[0] - 5, music_pos[1], 180, 30), (100, 100, 100))
    if is_text_hovered(exit_pos, 180, 30, mouse_pos):
        screen.draw.filled_rect(Rect(exit_pos[0] - 5, exit_pos[1], 180, 30), (100, 100, 100))

    # Desenha os textos do menu
    screen.draw.text("Roguelike", title_pos, fontsize=50)
    screen.draw.text("Encontre o Baú e fuja dos inimigos\n\nUse as setas do teclado para se mover", subtitle_pos, fontsize=18)
    screen.draw.text("(Clique na Opção Desejada)", menu_instrc_pos, fontsize=16)
    screen.draw.text("Iniciar", start_pos, fontsize=30)
    screen.draw.text("Som: " + ("LIGADO" if sound_on else "DESLIGADO"), music_pos, fontsize=30)
    screen.draw.text("Sair", exit_pos, fontsize=30)

    # Armazena as posições dos botões
    global button_positions
    button_positions = {
        "start": (start_pos, 120, 30),
        "music": (music_pos, 120, 30),
        "exit": (exit_pos, 120, 30)
    }

# Desenha o jogo
def draw_game():
    for row in range(16):
        for col in range(16):
            tile = map_layout[row][col]
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if tile == 0:
                screen.blit("floor", (x, y))
            elif tile == 1:
                screen.blit("wall", (x, y))

    goal.draw()
    hero.draw()
    for enemy in enemies:
        enemy.draw()

# Desenha vitória ou derrota
def draw_end_screen(text):
    screen.draw.text(text, center=(WIDTH // 2, 64), fontsize=32, color="white")
    screen.draw.text("Clique na tela para reiniciar", center=(WIDTH // 2, 140), fontsize=24, color="black")

# Detecta clique do mouse
def on_mouse_down(pos):
    global game_state, sound_on
    if game_state == MENU:
        if is_text_hovered(*button_positions["start"], pos):
            game_state = PLAYING
        elif is_text_hovered(*button_positions["music"], pos):
            sound_on = not sound_on
            if sound_on:
                sounds.background.play(True)
            else:
                sounds.background.stop()
        elif is_text_hovered(*button_positions["exit"], pos):
            exit()
    elif game_state in [VICTORY, DEFEAT]:
        new_game()

# Desenha as telas com base no estado do jogo
def draw():
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == VICTORY:
        draw_end_screen("Venceu")
    elif game_state == DEFEAT:
        draw_end_screen("O inimigo te alcançou,\nvocê perdeu")

# Atualiza o jogo em estado ativo
def update():
    global game_state
    if game_state == PLAYING:
        hero.move(keyboard, enemies, map_layout)
        for enemy in enemies:
            enemy.move(map_layout)

        # Verifica vitória
        if hero.actor.colliderect(goal):
            play_victory_sound()
            game_state = VICTORY

        # Verifica derrota
        for enemy in enemies:
            if hero.actor.colliderect(enemy.actor):
                play_defeat_sound()
                game_state = DEFEAT

# Reinicia o jogo
def new_game():
    global hero, enemies, goal, game_state
    hero = Hero(get_random_position(), 2)
    enemies = [Enemy(get_random_position(), 1) for _ in range(2)]
    goal = Actor('goal', get_random_position())
    game_state = MENU

# Inicia o jogo
new_game()

pgzrun.go()
