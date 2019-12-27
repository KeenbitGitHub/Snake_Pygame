import numpy
import random
import pygame

class Food:
    position = []
    
    def respawn(self, DONT_SPAWN_ARRAY, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT):
        x = random.randrange(0, int(WIN_SIZE[0]/BLOCK_WIDTH)) * BLOCK_WIDTH
        y = random.randrange(0, int(WIN_SIZE[1]/BLOCK_HEIGHT)) * BLOCK_HEIGHT
        self.position = [x, y] 
        if self.position in DONT_SPAWN_ARRAY:
            self.respawn(DONT_SPAWN_ARRAY, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT)
            
    def __init__(self, DONT_SPAWN_ARRAY, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT):
        self.respawn(DONT_SPAWN_ARRAY, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT)
    
    def render(self, BLOCK_WIDTH, BLOCK_HEIGHT, win):
        pygame.draw.rect(win, (230, 0, 0), (self.position[0], self.position[1], BLOCK_WIDTH, BLOCK_HEIGHT))