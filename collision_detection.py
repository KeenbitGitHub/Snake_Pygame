import numpy as np
import pygame


class collision_detector:
    
    # Detects collesion between snake and walls
    def snake_walls(self, snake_head, WIN_SIZE, BLOCK_SIZE):
        if (snake_head[0] < 0 or snake_head[0] > WIN_SIZE[0] - BLOCK_SIZE[0] or snake_head[1] < 0 or snake_head[1] > WIN_SIZE[1] - BLOCK_SIZE[1]):
            return True
        
    # Detects collesion between snake and food
    def snake_food(self, snake_head, food):
        if (snake_head[0] == food.position[0] and snake_head[1] == food.position[1]):
            return True
        
    # Detects collesion between snake and the snake itself
    def snake_suicide(self, snake_head, snake_body):
        if ((snake_head == snake_body[1:]).all(axis = 1).any()):
            return True
    
    # Detects collision
    def check_collision(self, snake_head, snake_body, WIN_SIZE, BLOCK_SIZE, food):
        # Returns 1 if wall is hit or snake bites itself
        # Returns 2 if snake eats food
        # Returns 3 if nothing happens
        if (self.snake_walls(snake_head, WIN_SIZE, BLOCK_SIZE) or self.snake_suicide(snake_head, snake_body)):
            return 1
        elif (self.snake_food(snake_head, food)):
            return 2
        else:
            return 3