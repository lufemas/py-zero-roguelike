import pgzrun
from pygame import Rect
import random
import math

# Tamanho da janela do jogo
WIDTH = 800
HEIGHT = 600

# Configurações do herói
hero = Actor('hero_down', (400, 300))  # Posição inicial do herói no centro da tela
hero_speed = 5

# Lista para inimigos
enemies = []

# Variáveis de estado
game_active = False
sound_on = True

def draw():
    screen.clear()
    if game_active:
        # Desenhar o mapa e os elementos do jogo
        draw_game()
    else:
        # Desenhar o menu principal
        draw_menu()

def update():
    if game_active:
        update_game()

def draw_game():
    hero.draw()
    # Desenhar inimigos
    for enemy in enemies:
        enemy.draw()

def update_game():
    move_hero()
    move_enemies()

def move_hero():
    if keyboard.left:
        hero.x -= hero_speed
        # hero.image = 'hero_left'
        hero.image = 'hero_down'
    elif keyboard.right:
        hero.x += hero_speed
        # hero.image = 'hero_right'
        hero.image = 'hero_down'
    elif keyboard.up:
        hero.y -= hero_speed
        # hero.image = 'hero_up'
        hero.image = 'hero_down'
    elif keyboard.down:
        hero.y += hero_speed
        hero.image = 'hero_down'

def move_enemies():
    # Exemplo básico de movimento aleatório para os inimigos
    for enemy in enemies:
        enemy.x += random.choice([-1, 1]) * 2
        enemy.y += random.choice([-1, 1]) * 2

def draw_menu():
    # Desenhar o menu com botões
    screen.draw.text("Roguelike Game", (WIDTH // 2 - 100, HEIGHT // 2 - 150), fontsize=50)
    screen.draw.text("Press SPACE to Start", (WIDTH // 2 - 150, HEIGHT // 2), fontsize=30)

def on_key_down(key):
    global game_active
    if key == keys.SPACE:
        game_active = True  # Inicia o jogo ao pressionar espaço

# Inicialização dos inimigos (só um exemplo, você pode adicionar mais lógica)
def setup_enemies():
    global enemies
    for _ in range(5):  # Adicionando 5 inimigos de exemplo
        enemy = Actor('enemy', (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
        enemies.append(enemy)

# Configuração inicial
setup_enemies()

pgzrun.go()
