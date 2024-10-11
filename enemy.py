from pgzero.actor import Actor
from pygame import Rect
import random
import time

class Enemy:
    def __init__(self, position, speed):
        self.actor = Actor('enemy_idle_0', position)  # Start with idle animation
        self.speed = speed
        self.moving = False
        self.target_position = position
        self.animation_frame = 0
        self.animation_time = time.time()
        self.actor.topleft = 0, 0
    
    def move(self, map_layout):
        if not self.moving:
            randomVal = random.random()
            print (randomVal);
            if randomVal < 0.90:  # 50% chance that the enemy won't move
                next_pos = None
            else:
                next_pos = self.choose_random_direction()

            if next_pos and self.can_move_to(next_pos, map_layout):
                self.target_position = next_pos
                self.moving = True

        # Move smoothly towards the target position
        if self.moving:
            self.smooth_move()

            if (self.actor.x, self.actor.y) == self.target_position:
                self.moving = False

        # Update sprite animation
        self.update_animation()

    def smooth_move(self):
        if self.actor.x < self.target_position[0]:
            self.actor.x += self.speed / 2  # Slow down the enemy movement
        elif self.actor.x > self.target_position[0]:
            self.actor.x -= self.speed / 2
        if self.actor.y < self.target_position[1]:
            self.actor.y += self.speed / 2
        elif self.actor.y > self.target_position[1]:
            self.actor.y -= self.speed / 2

    def choose_random_direction(self):
        directions = [
            (self.actor.x - 16, self.actor.y),  # Left
            (self.actor.x + 16, self.actor.y),  # Right
            (self.actor.x, self.actor.y - 16),  # Up
            (self.actor.x, self.actor.y + 16)   # Down
        ]
        return random.choice(directions)

    def can_move_to(self, position, map_layout):
        col, row = int(position[0] // 16), int(position[1] // 16)
        if col < 0 or row < 0 or col >= 16 or row >= 16:
            return False
        if map_layout[row][col] == 1:  # Collision with a wall
            return False
        return True

    def update_animation(self):
        current_time = time.time()
        if self.moving:
            if current_time - self.animation_time > 0.3:  # Change every 0.3 seconds
                self.animation_frame = (self.animation_frame + 1) % 2  # Toggle between 0 and 1
                self.actor.image = f'enemy_move_{self.animation_frame}'
                self.animation_time = current_time
        else:
            if current_time - self.animation_time > 0.5:  # Change every 0.5 seconds
                self.animation_frame = (self.animation_frame + 1) % 2
                self.actor.image = f'enemy_idle_{self.animation_frame}'
                self.animation_time = current_time

    def draw(self):
        self.actor.draw()