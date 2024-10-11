from pgzero.actor import Actor
from pygame import Rect
import random
import time

class Enemy:
    def __init__(self, position, speed):
        # Inicializa o inimigo com posição, velocidade e configurações de animação
        self.actor = Actor('enemy_idle_0', position)  # Começa com a animação de idle
        self.speed = speed  # Velocidade de movimento do inimigo
        self.moving = False  # Flag para verificar se o inimigo está se movendo
        self.target_position = position  # Posição alvo do inimigo
        self.animation_frame = 0  # Frame atual da animação
        self.animation_time = time.time()  # Controle de tempo para troca de frames
    
    def move(self, map_layout):
        # Controla o movimento aleatório do inimigo no mapa
        if not self.moving:
            randomVal = random.random()
            print(randomVal)
            
            # Define se o inimigo vai se mover com 90% de chance de não se mover
            if randomVal < 0.90:
                next_pos = None
            else:
                next_pos = self.choose_random_direction()

            # Verifica se a próxima posição é válida
            if next_pos and self.can_move_to(next_pos, map_layout):
                self.target_position = next_pos  # Define a posição alvo
                self.moving = True  # Inicia o movimento

        # Move suavemente em direção à posição alvo
        if self.moving:
            self.smooth_move()

            # Verifica se o inimigo chegou à posição alvo
            if (self.actor.x, self.actor.y) == self.target_position:
                self.moving = False

        # Atualiza a animação do inimigo
        self.update_animation()

    def smooth_move(self):
        # Move o inimigo suavemente em direção à posição alvo com velocidade reduzida
        if self.actor.x < self.target_position[0]:
            self.actor.x += self.speed / 2
        elif self.actor.x > self.target_position[0]:
            self.actor.x -= self.speed / 2
        if self.actor.y < self.target_position[1]:
            self.actor.y += self.speed / 2
        elif self.actor.y > self.target_position[1]:
            self.actor.y -= self.speed / 2

    def choose_random_direction(self):
        # Escolhe uma direção aleatória (esquerda, direita, cima ou baixo)
        directions = [
            (self.actor.x - 16, self.actor.y),  # Esquerda
            (self.actor.x + 16, self.actor.y),  # Direita
            (self.actor.x, self.actor.y - 16),  # Cima
            (self.actor.x, self.actor.y + 16)   # Baixo
        ]
        return random.choice(directions)  # Retorna uma direção aleatória

    def can_move_to(self, position, map_layout):
        # Verifica se a nova posição é válida e não contém uma parede
        col, row = int(position[0] // 16), int(position[1] // 16)
        if col < 0 or row < 0 or col >= 16 or row >= 16:  # Fora dos limites do mapa
            return False
        if map_layout[row][col] == 1:  # Colisão com uma parede
            return False
        return True

    def update_animation(self):
        # Atualiza a animação do inimigo, alternando entre os frames
        current_time = time.time()
        if self.moving:
            # Troca de frame a cada 0.3 segundos enquanto o inimigo se move
            if current_time - self.animation_time > 0.3:
                self.animation_frame = (self.animation_frame + 1) % 2  # Alterna entre os frames de movimento
                self.actor.image = f'enemy_move_{self.animation_frame}'
                self.animation_time = current_time
        else:
            # Troca de frame a cada 0.5 segundos enquanto o inimigo está parado
            if current_time - self.animation_time > 0.5:
                self.animation_frame = (self.animation_frame + 1) % 2  # Alterna entre os frames de idle
                self.actor.image = f'enemy_idle_{self.animation_frame}'
                self.animation_time = current_time

    def draw(self):
        # Desenha o inimigo na tela
        self.actor.draw()
