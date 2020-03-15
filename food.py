import numpy as np
import random
import pygame

class Food:
    position = []
    
    # spawns a piece of food
    def respawn(self, DONT_SPAWN_ARRAY, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT):
        x = random.randrange(0, int(WIN_SIZE[0]/BLOCK_WIDTH)) * BLOCK_WIDTH
        y = random.randrange(0, int(WIN_SIZE[1]/BLOCK_HEIGHT)) * BLOCK_HEIGHT
        self.position = np.array([x, y])
        if ((self.position == DONT_SPAWN_ARRAY).all(axis = 1).any()):
            self.respawn(DONT_SPAWN_ARRAY, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT)
       
    def __init__(self, DONT_SPAWN_ARRAY, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT):
        self.respawn(DONT_SPAWN_ARRAY, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT)
    
    # Renders a piece of food
    def render(self, BLOCK_WIDTH, BLOCK_HEIGHT, win):
        pygame.draw.rect(win, (230, 0, 0), (self.position[0], self.position[1], BLOCK_WIDTH, BLOCK_HEIGHT))
        
    def dead_render(self, BLOCK_WIDTH, BLOCK_HEIGHT, win):
        pygame.draw.rect(win, (0, 0, 0), (self.position[0], self.position[1], BLOCK_WIDTH, BLOCK_HEIGHT))