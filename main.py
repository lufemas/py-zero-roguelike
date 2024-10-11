from hero import Hero
from enemy import Enemy
import pgzrun
import random
import pygame

# Dimensões do mapa (16x16 tiles, cada um com 16x16 pixels)
WIDTH = 256
HEIGHT = 256
TILE_SIZE = 16

# Estado do jogo
game_active = False
victory = False
defeat = False
sound_on = True

# Sons
sounds.background.play(True)  # Música de fundo

# Mapa: 0 = chão, 1 = parede
map_layout = [[0 if random.random() > 0.2 else 1 for _ in range(16)] for _ in range(16)]

# Função para obter uma posição aleatória que não seja uma parede
def get_random_position():
    while True:
        x, y = random.randint(0, 15) * TILE_SIZE, random.randint(0, 15) * TILE_SIZE
        col, row = x // TILE_SIZE, y // TILE_SIZE
        if map_layout[row][col] == 0:  # Não é parede
            return (x+8, y+8)

# Funções para tocar sons específicos
def play_victory_sound():
    if sound_on:
        sounds.victory.play()

def play_defeat_sound():
    if sound_on:
        sounds.defeat.play()

# Função para verificar se o clique ocorreu em uma área do texto
def is_text_hovered(text_pos, text_width, text_height, mouse_pos):
    x, y = text_pos
    return x < mouse_pos[0] < x + text_width and y < mouse_pos[1] < y + text_height

# Função para desenhar o menu com botões clicáveis
def draw_menu():
    screen.clear()
    title_pos = (WIDTH // 2 - 100, HEIGHT // 2 - 150)
    start_pos = (WIDTH // 2 - 60, HEIGHT // 2)
    music_pos = (WIDTH // 2 - 60, HEIGHT // 2 + 50)
    exit_pos = (WIDTH // 2 - 60, HEIGHT // 2 + 100)

    # Verificar se o mouse está sobre os botões
    mouse_pos = pygame.mouse.get_pos()

    if is_text_hovered(start_pos, 120, 30, mouse_pos):
        screen.draw.filled_rect(Rect(start_pos[0] - 5, start_pos[1], 130, 30), 'gray')
    if is_text_hovered(music_pos, 120, 30, mouse_pos):
        screen.draw.filled_rect(Rect(music_pos[0] - 5, music_pos[1], 130, 30), 'gray')
    if is_text_hovered(exit_pos, 120, 30, mouse_pos):
        screen.draw.filled_rect(Rect(exit_pos[0] - 5, exit_pos[1], 130, 30), 'gray')

    # Desenhar os textos
    screen.draw.text("Roguelike Game", title_pos, fontsize=50)
    screen.draw.text("Start Game", start_pos, fontsize=30)
    screen.draw.text("Music: " + ("On" if sound_on else "Off"), music_pos, fontsize=30)
    screen.draw.text("Exit", exit_pos, fontsize=30)

    # Salvar posições dos textos para detecção de cliques
    global button_positions
    button_positions = {
        "start": (start_pos, 120, 30),  # (posição, largura, altura)
        "music": (music_pos, 120, 30),
        "exit": (exit_pos, 120, 30)
    }

# Função para checar se o botão foi clicado
def on_mouse_down(pos):
    global game_active, sound_on
    if not game_active:
        if victory or defeat:
            new_game()  # Volta para o menu inicial ao clicar na tela de vitória ou derrota
        else:
            # Verificar se o clique foi em um dos botões
            if is_text_hovered(*button_positions["start"], pos):
                game_active = True  # Começar o jogo
            elif is_text_hovered(*button_positions["music"], pos):
                sound_on = not sound_on  # Ligar/desligar música
                if sound_on:
                    sounds.background.play(loop=True)
                else:
                    sounds.background.stop()
            elif is_text_hovered(*button_positions["exit"], pos):
                exit()  # Sair do jogo

def draw():
    screen.clear()
    if not game_active:
        if victory:
            screen.draw.text("Venceu", center=(WIDTH // 2, HEIGHT // 2), fontsize=50, color="white")
        elif defeat:
            screen.draw.text("O inimigo te alcançou, você perdeu", center=(WIDTH // 2, HEIGHT // 2), fontsize=30, color="white")
        else:
            draw_menu()
    else:
        draw_game()

def draw_game():
    # Desenhar o mapa
    for row in range(16):
        for col in range(16):
            tile = map_layout[row][col]
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if tile == 0:
                screen.blit("floor", (x, y))
            elif tile == 1:
                screen.blit("wall", (x, y))

    # Desenhar o goal
    goal.draw()

    # Desenhar o herói e os inimigos
    hero.draw()
    for enemy in enemies:
        enemy.draw()

def update():
    global game_active, victory, defeat

    if game_active:
        hero.move(keyboard, enemies, map_layout)
        for enemy in enemies:
            enemy.move(map_layout)

        # Verificar colisão com o goal
        if hero.actor.colliderect(goal):
            victory = True
            play_victory_sound()
            game_active = False

        # Verificar colisão com os inimigos
        for enemy in enemies:
            if hero.actor.colliderect(enemy.actor):
                defeat = True
                play_defeat_sound()
                game_active = False

def on_key_down(key):
    global game_active, victory, defeat
    if key == keys.SPACE:
        if not game_active and (victory or defeat):
            new_game()
        else:
            game_active = True  # Iniciar o jogo

# Função para resetar o jogo
def new_game():
    global hero, enemies, goal, victory, defeat
    hero = Hero(get_random_position(), 2)
    enemies = [Enemy(get_random_position(), 2) for _ in range(2)]
    goal = Actor('goal', get_random_position())
    game_active = False
    victory = False
    defeat = False

# Iniciar o novo jogo ao iniciar
new_game()

pgzrun.go()
