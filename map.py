import random

TILE_SIZE = 16

def generate_map():
    print("[map.py] Gerando mapa")
    # Gera o layout do mapa com 0 = chão e 1 = parede
    return [[0 if random.random() > 0.2 else 1 for _ in range(16)] for _ in range(16)]

def get_random_position(map_layout):
    while True:
        x, y = random.randint(0, len(map_layout[0]) - 1) * TILE_SIZE, random.randint(0, len(map_layout[1]) - 1) * TILE_SIZE
        col, row = x // TILE_SIZE, y // TILE_SIZE
        if map_layout[row][col] == 0:
            return (x + (TILE_SIZE/2), y + (TILE_SIZE/2))
