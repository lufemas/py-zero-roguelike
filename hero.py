from pgzero.actor import Actor
from pygame import Rect
import time

class Hero:
    def __init__(self, position, speed):
        print("POSITION:", position)
        self.actor = Actor('hero_idle_0', (80,80))
        self.actor.x = position[0]
        self.actor.y = position[1]
        print("self.actor.y", self.actor.y)
        # self.actor = Actor('hero_idle_0', position)
        self.speed = speed
        self.moving = False
        self.target_position = position
        # self.actor.topleft = 0, 0
        self.animation_frame = 0
        self.animation_time = time.time()
    
    def move(self, keyboard, enemies, map_layout):
        # Allow movement only if not already moving
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
            self.actor.x += self.speed
        elif self.actor.x > self.target_position[0]:
            self.actor.x -= self.speed
        if self.actor.y < self.target_position[1]:
            self.actor.y += self.speed
        elif self.actor.y > self.target_position[1]:
            self.actor.y -= self.speed

    def can_move_to(self, position, map_layout):
        col, row = int(position[0] // 16), int(position[1] // 16)  # Ensure integers
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
                self.actor.image = f'hero_move_{self.animation_frame}'
                self.animation_time = current_time
        else:
            if current_time - self.animation_time > 0.5:  # Change every 0.5 seconds
                self.animation_frame = (self.animation_frame + 1) % 2
                self.actor.image = f'hero_idle_{self.animation_frame}'
                self.animation_time = current_time

    def draw(self):
        self.actor.draw()