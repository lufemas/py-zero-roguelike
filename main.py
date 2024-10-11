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
sound_on = True

# Mapa: 0 = chão, 1 = parede
map_layout = [[0 if random.random() > 0.2 else 1 for _ in range(16)] for _ in range(16)]

# Inicializar o herói e os inimigos
hero = Hero((16, 16), 2)  # Começa no segundo tile
enemies = [Enemy((224, 224), 2), Enemy((96, 96), 2)]  # Colocar os inimigos em posições diferentes

def draw():
    # screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    # screen.surface = pygame.display.set_mode((WIDTH * 2, HEIGHT * 2), pygame.SCALED)
    screen.clear()
    if game_active:
        draw_game()
    else:
        draw_menu()

def draw_menu():
    screen.draw.text("Roguelike Game", (WIDTH // 2 - 100, HEIGHT // 2 - 150), fontsize=50)
    screen.draw.text("Press SPACE to Start", (WIDTH // 2 - 150, HEIGHT // 2), fontsize=30)

debug = True  # Toggle this to False to disable debug borders

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
    
    # Desenhar o herói e os inimigos
    hero.draw()
    if debug:
        draw_sprite_border(hero.actor)  # Draw border for the hero

    for enemy in enemies:
        enemy.draw()
        if debug:
            draw_sprite_border(enemy.actor)  # Draw border for each enemy

def update():
    if game_active:
        update_game()

def update_game():
    hero.move(keyboard, enemies, map_layout)  # Passar o layout do mapa para o herói verificar colisões
    for enemy in enemies:
        enemy.move(map_layout)

def on_key_down(key):
    global game_active
    if key == keys.SPACE:
        game_active = True  # Iniciar o jogo

def draw_sprite_border(sprite):
    # Draw a red rectangle around the sprite for debugging purposes
    screen.draw.rect(Rect(sprite.left, sprite.top, sprite.width, sprite.height), 'red')
pgzrun.go()
