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

# Mapa: 0 = chão, 1 = parede
map_layout = [[0 if random.random() > 0.2 else 1 for _ in range(16)] for _ in range(16)]

# Função para obter uma posição aleatória que não seja uma parede
def get_random_position():
    while True:
        x, y = random.randint(0, 15) * TILE_SIZE, random.randint(0, 15) * TILE_SIZE
        print("Sorteado", x,y)
        col, row = x // TILE_SIZE, y // TILE_SIZE
        print(" col, row",  col, row)
        if map_layout[row][col] == 0:  # Não é parede
            print("Nao e parede", x,y)

            return (x, y)

# Inicializar o herói, inimigos, e o objetivo (goal)
# hero = Hero(get_random_position(), 2)
# enemies = [Enemy(get_random_position(), 2) for _ in range(1)]
# goal = Actor('goal', get_random_position())  # O objetivo também é aleatório
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

def draw_menu():
    screen.draw.text("Roguelike Game", (WIDTH // 2 - 100, HEIGHT // 2 - 150), fontsize=50)
    screen.draw.text("Press SPACE to Start", (WIDTH // 2 - 150, HEIGHT // 2), fontsize=30)

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
            game_active = False

        # Verificar colisão com os inimigos
        for enemy in enemies:
            if hero.actor.colliderect(enemy.actor):
              print("COLIDIU")
                # defeat = True
                # game_active = False

def on_key_down(key):
    global game_active, victory, defeat
    if key == keys.SPACE:
        if not game_active and (victory or defeat):
            reset_game()  # Reiniciar o jogo após vitória ou derrota
        else:
            game_active = True  # Iniciar o jogo

# Função para resetar o jogo
def reset_game():
    global hero, enemies, goal, victory, defeat
    hero = Hero(get_random_position(), 2)
    enemies = [Enemy(get_random_position(), 2) for _ in range(1)]
    goal = Actor('goal', get_random_position())
    game_active = True
    victory = False
    defeat = False

reset_game()

pgzrun.go()
