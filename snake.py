import pygame
import numpy as np

class Snake:
    # Structure of snake: [head, body, body, ...,  tail]
    body = None
    head = None
    alive = False
    moved_from = [None, None]
    
    def __init__(self, start_pos, snake_len, BLOCK_SIZE):
        self.spawn(start_pos, snake_len, BLOCK_SIZE)
        
    # Spawns snake
    def spawn(self, start_pos, snake_len, BLOCK_SIZE):
        self.alive = True
        self.body = (np.array([start_pos[0] - 1 * BLOCK_SIZE[0], start_pos[1]])).reshape((-1, 2))
        self.head = self.body[0]
        for i in range(2, snake_len + 2):
            self.body = (np.append(self.body, [start_pos[0] - i * BLOCK_SIZE[0], start_pos[1]])).reshape((-1, 2))
       
    # Moves snake
    def move(self, direction, speed):
        self.head = np.add(self.head, np.array([direction[0] * speed[0], direction[1] * speed[1]]))
        last_element = self.body[-1]
        self.body[1:] = self.body[:-1]
        self.body[0] = self.head
        self.moved_from = last_element
        
    # Renders snake
    def render(self, BLOCK_WIDTH, BLOCK_HEIGHT, win):
        pygame.draw.rect(win, (0, 200, 0), (self.head[0], self.head[1], BLOCK_WIDTH, BLOCK_HEIGHT))
            
        for part in self.body[1:]:
            pygame.draw.rect(win, (0, 255, 0), (part[0], part[1], BLOCK_WIDTH, BLOCK_HEIGHT))
        
        pygame.draw.rect(win, (0, 0, 0), (self.moved_from[0], self.moved_from[1], BLOCK_WIDTH, BLOCK_HEIGHT))
        
    def dead_render(self, BLOCK_WIDTH, BLOCK_HEIGHT, win):
        pygame.draw.rect(win, (0, 0, 0), (self.head[0], self.head[1], BLOCK_WIDTH, BLOCK_HEIGHT))
            
        for part in self.body[1:]:
            pygame.draw.rect(win, (0, 0, 0), (part[0], part[1], BLOCK_WIDTH, BLOCK_HEIGHT))
        
        pygame.draw.rect(win, (0, 0, 0), (self.moved_from[0], self.moved_from[1], BLOCK_WIDTH, BLOCK_HEIGHT))