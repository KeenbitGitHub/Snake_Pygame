import pygame
import numpy as np

class Snake:
    # [head, body, body, ...,  tail]
    body = None
    head = None
    alive = False
    moved_from = [None, None]
    
    def __init__(self, start_pos, snake_len):
        self.spawn(start_pos, snake_len)
        
    def spawn(self, start_pos, snake_len):
        self.alive = True
        self.head = np.array(start_pos)
        self.body = (np.array([start_pos[0] - 1, start_pos[1]])).reshape((-1, 2))
        for i in range(2, snake_len + 1):
            self.body = (np.append(self.body, [start_pos[0] - i, start_pos[1]])).reshape((-1, 2))
    
    def eat(self):
        pass
    
    def move(self, direction, speed):
        self.head = np.add(self.head, np.array([direction[0] * speed[0], direction[1] * speed[1]]))
        last_element = self.body[-1]
        self.body[1:] = self.body[:-1]
        self.body[0] = self.head
        self.moved_from = last_element
    
    def die(self):
        pass