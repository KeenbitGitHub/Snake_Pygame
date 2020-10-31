import numpy as np
import pygame
import game
from NeuralNetwork.NeuralNetwork import NeuralNetwork

class candidate:
    def __init__(self):
        self.nn = NeuralNetwork(12)
        self.nn.add_layer(12, activation = "relu")
        self.nn.add_layer(4)
        self.game_instance = game.Game(False)
        self.available_moves = 200
        self.fitness = 0
        self.lifetime = 0
    
    def look_left(self):
        food_dist = 0
        wall_dist = 1/((self.game_instance.snake_instance.head[0]/self.game_instance.BLOCK_WIDTH) + 1/self.game_instance.BLOCK_WIDTH)
        body_dist = 0
        for x in reversed(range(0, self.game_instance.snake_instance.head[0], self.game_instance.BLOCK_WIDTH)):
            if (x == self.game_instance.food_instance.position[0] and self.game_instance.snake_instance.head[1] == self.game_instance.food_instance.position[1]):
                food_dist = 1/((self.game_instance.snake_instance.head[0] - x)/self.game_instance.BLOCK_WIDTH)
            
            if (x in self.game_instance.snake_instance.body[1:, 0] and self.game_instance.snake_instance.head[1] in self.game_instance.snake_instance.body[1:, 1]):
                body_dist = 1/(((self.game_instance.snake_instance.head[0] - x)/self.game_instance.BLOCK_WIDTH) + 1/(self.game_instance.BLOCK_WIDTH))
        
        return food_dist, wall_dist, body_dist
    
    def look_right(self):
        food_dist = 0
        wall_dist = 1/(((self.game_instance.WIN_WIDTH - self.game_instance.snake_instance.head[0])/self.game_instance.BLOCK_WIDTH) + 1/self.game_instance.BLOCK_WIDTH)
        body_dist = 0
        for x in range(self.game_instance.snake_instance.head[0], self.game_instance.WIN_WIDTH, self.game_instance.BLOCK_WIDTH):
            if (x == self.game_instance.food_instance.position[0] and self.game_instance.snake_instance.head[1] == self.game_instance.food_instance.position[1]):
                food_dist = 1/((x - self.game_instance.snake_instance.head[0])/self.game_instance.BLOCK_WIDTH)
            
            if (x in self.game_instance.snake_instance.body[1:, 0] and self.game_instance.snake_instance.head[1] in self.game_instance.snake_instance.body[1:, 1]):
                body_dist = 1/(((x - self.game_instance.snake_instance.head[0])/self.game_instance.BLOCK_WIDTH) + 1/(self.game_instance.BLOCK_WIDTH))
        
        return food_dist, wall_dist, body_dist
    
    def look_up(self):
        food_dist = 0
        wall_dist = 1/((self.game_instance.snake_instance.head[1]/self.game_instance.BLOCK_HEIGHT) + 1/self.game_instance.BLOCK_HEIGHT)
        body_dist = 0
        for y in reversed(range(0, self.game_instance.snake_instance.head[1], self.game_instance.BLOCK_HEIGHT)):
            if (self.game_instance.snake_instance.head[0] == self.game_instance.food_instance.position[0] and y == self.game_instance.food_instance.position[1]):
                food_dist = 1/((self.game_instance.snake_instance.head[1] - y)/self.game_instance.BLOCK_HEIGHT)
            
            if (y in self.game_instance.snake_instance.body[1:, 1] and self.game_instance.snake_instance.head[0] in self.game_instance.snake_instance.body[1:, 0]):
                body_dist = 1/(((self.game_instance.snake_instance.head[1] - y)/self.game_instance.BLOCK_HEIGHT) + 1/(self.game_instance.BLOCK_HEIGHT))
        
        return food_dist, wall_dist, body_dist

    def look_down(self):
        food_dist = 0
        wall_dist = 1/(((self.game_instance.WIN_HEIGHT - self.game_instance.snake_instance.head[1])/self.game_instance.BLOCK_HEIGHT) + 1/self.game_instance.BLOCK_HEIGHT)
        body_dist = 0
        for y in range(self.game_instance.snake_instance.head[1], self.game_instance.WIN_HEIGHT, self.game_instance.BLOCK_HEIGHT):
            if (self.game_instance.snake_instance.head[0] == self.game_instance.food_instance.position[0] and y == self.game_instance.food_instance.position[1]):
                food_dist = 1/((y - self.game_instance.snake_instance.head[1])/self.game_instance.BLOCK_HEIGHT)

            elif (y in self.game_instance.snake_instance.body[1:, 1] and self.game_instance.snake_instance.head[0] in self.game_instance.snake_instance.body[1:, 0]):
                body_dist = 1/(((y - self.game_instance.snake_instance.head[1])/self.game_instance.BLOCK_HEIGHT) + 1/(self.game_instance.BLOCK_HEIGHT))
        
        return food_dist, wall_dist, body_dist
        
    def feedforward(self):
        up = self.look_up()
        down = self.look_down()
        left = self.look_left()
        right = self.look_right()
        data = [up[0], up[1], up[2], down[0], down[1], down[2], left[0], left[1], left[2], right[0], right[1], right[2]]
        pred = self.nn.predict(np.array(data))
        return np.argmax(pred)
        
    def move(self):
        if (self.game_instance.human_playes):
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    self.game_running = False
                    self.UPDATE_SPEED = 0
                    break
                elif (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT and self.game_instance.direction != (1, 0) and not self.game_instance.update_move):
                        self.game_instance.direction = (-1, 0)
                        self.game_instance.update_move = True
                    elif (event.key == pygame.K_RIGHT and self.game_instance.direction != (-1, 0) and not self.game_instance.update_move):
                        self.game_instance.direction = (1, 0)
                        self.game_instance.update_move = True
                    elif (event.key == pygame.K_DOWN and self.game_instance.direction != (0, -1) and not self.game_instance.update_move):
                        self.game_instance.direction = (0, 1)
                        self.game_instance.update_move = True
                    elif (event.key == pygame.K_UP and self.game_instance.direction != (0, 1) and not self.game_instance.update_move):
                        self.game_instance.direction = (0, -1)
                        self.game_instance.update_move = True
        else:
            move = self.feedforward()
            
            if (move == 0 and self.game_instance.direction != (1, 0) and not self.game_instance.update_move):
                self.game_instance.direction = (-1, 0)
                self.game_instance.update_move = True
            elif (move == 1 and self.game_instance.direction != (-1, 0) and not self.game_instance.update_move):
                self.game_instance.direction = (1, 0)
                self.game_instance.update_move = True
            elif (move == 2 and self.game_instance.direction != (0, -1) and not self.game_instance.update_move):
                self.game_instance.direction = (0, 1)
                self.game_instance.update_move = True
            elif (move == 3 and self.game_instance.direction != (0, 1) and not self.game_instance.update_move):
                self.game_instance.direction = (0, -1)
                self.game_instance.update_move = True
                
            self.game_instance.main()
        
    def run(self):
        while (self.game_instance.snake_instance.alive):
            old_score = self.game_instance.score
            self.move()
            new_score = self.game_instance.score
            
            if (old_score != new_score):
                self.available_moves += 100
                if (self.available_moves > 500):
                    self.available_moves = 500

            self.available_moves -= 1
            
            if (self.available_moves < 1):
                self.game_instance.snake_instance.alive = False
            
            self.lifetime += 1
            
        self.fitness = self.lifetime * 2**self.game_instance.score
        
        self.game_instance.clear_screen()