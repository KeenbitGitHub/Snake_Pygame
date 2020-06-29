"""
Baseline based on random movement.
"""

import numpy as np
import pygame
import game

game_instance = game.Game(False)

while game_instance.snake_instance.alive:
    rnd = np.random.randint(0, 4)
    if (rnd == 0 and game_instance.direction != (1, 0) and not game_instance.update_move):
        game_instance.direction = (-1, 0)
        game_instance.update_move = True
    elif (rnd == 1 and game_instance.direction != (-1, 0) and not game_instance.update_move):
        game_instance.direction = (1, 0)
        game_instance.update_move = True
    elif (rnd == 2 and game_instance.direction != (0, -1) and not game_instance.update_move):
        game_instance.direction = (0, 1)
        game_instance.update_move = True
    elif (rnd == 3 and game_instance.direction != (0, 1) and not game_instance.update_move):
        game_instance.direction = (0, -1)
        game_instance.update_move = True
        
    game_instance.main()