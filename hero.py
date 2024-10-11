from pgzero.actor import Actor
from pygame import Rect
import time

class Hero:
    def __init__(self, position, speed):
        # Inicializa o herói com sua posição inicial, velocidade e configurações de animação
        print("POSITION:", position)
        self.actor = Actor('hero_idle_0', (80, 80))  # Inicializa com a imagem 'hero_idle_0'
        self.actor.x = position[0]
        self.actor.y = position[1]
        self.speed = speed  # Velocidade de movimento do herói
        self.moving = False  # Flag para verificar se o herói está se movendo
        self.target_position = position  # Posição alvo do herói
        self.animation_frame = 0  # Frame atual da animação do herói
        self.animation_time = time.time()  # Tempo inicial para controlar a troca de frames

    def move(self, keyboard, enemies, map_layout):
        # Controla o movimento do herói com base nas teclas pressionadas
        if not self.moving:
            next_pos = None

            if keyboard.left:
                next_pos = (self.actor.x - 16, self.actor.y)  
            elif keyboard.right:
                next_pos = (self.actor.x + 16, self.actor.y)
            elif keyboard.up:
                next_pos = (self.actor.x, self.actor.y - 16)
            elif keyboard.down:
                next_pos = (self.actor.x, self.actor.y + 16)
            
            # Verifica se a próxima posição é válida para o movimento
            if next_pos and self.can_move_to(next_pos, map_layout):
                self.target_position = next_pos  # Define a posição alvo
                self.moving = True  # Inicia o movimento

        # Movimenta o herói suavemente até a posição alvo
        if self.moving:
            self.smooth_move()

            # Verifica se o herói chegou à posição alvo
            if (self.actor.x, self.actor.y) == self.target_position:
                self.moving = False

        # Atualiza a animação do herói
        self.update_animation()

    def smooth_move(self):
        # Move o herói suavemente na direção da posição alvo
        if self.actor.x < self.target_position[0]:
            self.actor.x += self.speed
        elif self.actor.x > self.target_position[0]:
            self.actor.x -= self.speed
        if self.actor.y < self.target_position[1]:
            self.actor.y += self.speed
        elif self.actor.y > self.target_position[1]:
            self.actor.y -= self.speed

    def can_move_to(self, position, map_layout):
        # Verifica se a posição desejada é válida, ou seja, dentro do mapa e sem colisão com uma parede
        col, row = int(position[0] // 16), int(position[1] // 16)  # Converte as coordenadas em células de 16x16
        if col < 0 or row < 0 or col >= 16 or row >= 16:  # Verifica se está fora dos limites do mapa
            return False
        if map_layout[row][col] == 1:  # Verifica se a célula é uma parede
            return False
        return True

    def update_animation(self):
        # Atualiza a animação do herói dependendo se ele está se movendo ou parado
        current_time = time.time()
        if self.moving:
            # Troca de frame a cada 0.2 segundos enquanto se move
            if current_time - self.animation_time > 0.2:
                self.animation_frame = (self.animation_frame + 1) % 2  # Alterna entre os frames de movimento
                self.actor.image = f'hero_move_{self.animation_frame}'
                self.animation_time = current_time
        else:
            # Troca de frame a cada 0.5 segundos enquanto está parado
            if current_time - self.animation_time > 0.25:
                self.animation_frame = (self.animation_frame + 1) % 2  # Alterna entre os frames de idle
                self.actor.image = f'hero_idle_{self.animation_frame}'
                self.animation_time = current_time

    def draw(self):
        # Desenha o herói na tela
        self.actor.draw()
