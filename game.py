import pygame
import snake
import food
import collision_detection
import numpy as np
from NeuralNetwork import NeuralNetwork as nn

class Game:
    def __init__(self, simulate, human_plays, pop_size = 1, fitness = 0):
        self.initialize(simulate, human_plays, fitness, pop_size)
        
        if (self.human_plays):
            self.main()
        else:
            model = nn.NeuralNetwork(12)
            model.add_layer(16)
            model.add_layer(16)
            model.add_layer(4)
            
            """
            The neural network takes the following inputs:
                0) How far the snake can move to the left before hitting an object
                1) How far the snake can move to the right before hitting an object
                2) How far the snake can move to the up before hitting an object
                3) How far the snake can move to the down before hitting an object
                4) If the object to the left (of the head of the snake) is food
                5) If the object to the left (of the head of the snake) is wall/the snake itself
                6) If the object to the right (of the head of the snake) is food
                7) If the object to the right (of the head of the snake) is a wall/the snake itself
                8) If the object to the up (of the head of the snake) is food
                9) If the object to the up (of the head of the snake) is a wall/the snake itself
                10) If the object to the down (of the head of the snake) is food
                11) If the object to the down (of the head of the snake) is a wall/the snake itself
                12) If the snake is going left
                13) If the snake is going right
                14) If the snake is going up
                15) If the snake is going down
                
            And has the following output:
                1) (1) if the snake is going to the left, (0) if not
                2) (1) if the snake is going to the right, (0) if not
                3) (1) if the snake is going to the up, (0) if not
                4) (1) if the snake is going to the down, (0) if not
            """
    
    # Initializes variables
    def initialize(self, simulate, human_plays, fitness, pop_size):
        self.simulate = simulate
        self.human_plays = human_plays
        self.BLOCK_WIDTH, self.BLOCK_HEIGHT = 50, 50 
        self.BLOCK_SIZE = (self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.WIN_WIDTH, self.WIN_HEIGHT = 800, 800
        self.WIN_SIZE = (self.WIN_WIDTH, self.WIN_HEIGHT)
        self.direction = (1, 0)
        self.snake_instance = snake.Snake((self.WIN_WIDTH/2, self.WIN_HEIGHT/2), 4, self.BLOCK_SIZE)
        self.food_instance = food.Food(self.snake_instance.body, self.WIN_SIZE, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.collision_detection_instance = collision_detection.collision_detector()
        self.win = pygame.display.set_mode(self.WIN_SIZE)
        self.game_running = True
        self.fitness = fitness
        self.pop_size = pop_size
        self.available_moves = 25
        self.nn_input = np.zeros((1, 12))
        
        pygame.init()
        
        if (self.simulate):
            self.CAPTION = "AI plays snake"
            pygame.display.set_caption(self.CAPTION)
        
    # Checks for player input
    def player_input(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.game_running = False
                self.UPDATE_SPEED = 0
                break
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT and self.direction != (1, 0) and not self.update_move):
                    self.direction = (-1, 0)
                    self.update_move = True
                elif (event.key == pygame.K_RIGHT and self.direction != (-1, 0) and not self.update_move):
                    self.direction = (1, 0)
                    self.update_move = True
                elif (event.key == pygame.K_DOWN and self.direction != (0, -1) and not self.update_move):
                    self.direction = (0, 1)
                    self.update_move = True
                elif (event.key == pygame.K_UP and self.direction != (0, 1) and not self.update_move):
                    self.direction = (0, -1)
                    self.update_move = True
        
    # Renders game
    def render(self):
        self.food_instance.render(self.BLOCK_WIDTH, self.BLOCK_HEIGHT, self.win)
        self.snake_instance.render(self.BLOCK_WIDTH, self.BLOCK_HEIGHT, self.win)
        pygame.display.update()
        
    # Checks for collision
    def collision(self):
        col_result = self.collision_detection_instance.check_collision(self.snake_instance.head, 
            self.snake_instance.body, self.WIN_SIZE, self.BLOCK_SIZE, self.food_instance)
        
        if (col_result == 1): # Wall is hit or snake bites itself
            self.snake_instance.alive = False
        elif (col_result == 2): # If snake eats food
            self.food_instance.respawn(self.snake_instance.body, self.WIN_SIZE, self.BLOCK_SIZE[0], self.BLOCK_SIZE[1])
            self.snake_instance.body = np.append(self.snake_instance.body, self.snake_instance.moved_from).reshape((-1, 2))
            self.fitness += 500
            self.available_moves += 25
            
    def set_nn_input(self):
        def set_input_0():
            for x in reversed(range(0, int(self.snake_instance.head[0]), self.BLOCK_WIDTH)):
                if (x == self.food_instance.position[0] and self.snake_instance.head[1] == self.food_instance.position[1]):
                    return self.snake_instance.head[0] - x
                # NEEDS TO CHECK FOR SNAKE BODY
            return self.snake_instance.head[0]
        
        def set_input_1():
            for x in range(int(self.snake_instance.head[0]), self.WIN_WIDTH, self.BLOCK_WIDTH):
                if (x == self.food_instance.position[0] and self.snake_instance.head[1] == self.food_instance.position[1]):
                    return x - self.snake_instance.head[0]
                # NEEDS TO CHECK FOR SNAKE BODY
            return self.WIN_WIDTH - self.snake_instance.head[0]
        
        def set_input_2():
            for y in reversed(range(0, int(self.snake_instance.head[1]), self.BLOCK_WIDTH)):
                if (y == self.food_instance.position[1] and self.snake_instance.head[0] == self.food_instance.position[0]):
                    return self.snake_instance.head[1] - y
                # NEEDS TO CHECK FOR SNAKE BODY
            return self.snake_instance.head[1]
        
        def set_input_3():
            for y in range(int(self.snake_instance.head[1]), self.WIN_HEIGHT, self.BLOCK_WIDTH):
                if (y == self.food_instance.position[1] and self.snake_instance.head[0] == self.food_instance.position[0]):
                    return y - self.snake_instance.head[1]
                # NEEDS TO CHECK FOR SNAKE BODY
            return self.WIN_HEIGHT - self.snake_instance.head[1]
        
        # Sets inut 12 - 15
        if (self.direction[0] == -1 and self.direction[1] == 0):
            self.nn_input[0, 12] = 1
            self.nn_input[0, 13] = 0
            self.nn_input[0, 14] = 0
            self.nn_input[0, 15] = 0
        elif (self.direction[0] == 1 and self.direction[1] == 0):
            self.nn_input[0, 12] = 0
            self.nn_input[0, 13] = 1
            self.nn_input[0, 14] = 0
            self.nn_input[0, 15] = 0
        elif (self.direction[0] == 0 and self.direction[1] == 1):
            self.nn_input[0, 12] = 0
            self.nn_input[0, 13] = 0
            self.nn_input[0, 14] = 0
            self.nn_input[0, 15] = 1
        elif (self.direction[0] == 0 and self.direction[1] == -1):
            self.nn_input[0, 12] = 0
            self.nn_input[0, 13] = 0
            self.nn_input[0, 14] = 1
            self.nn_input[0, 15] = 0

    # Starts the game and the game-loop
    def main(self):
        self.update_move = False
        self.UPDATE_SPEED = int(200/self.pop_size)
        
        self.fitness += 10
        
        """NEED TO BE UNCOMMENTED - COMMENTED FOR TESTING"""
        #self.available_moves -= 1 
        
        if (self.available_moves <= 0):
            self.snake_instance.alive = False
        
        if (self.human_plays):
            self.player_input()
            
            """NEED TO BE REMOVED - ADDED FOR TESTING"""
            self.set_nn_input() 
        else:
            self.set_nn_input()
            
        self.snake_instance.move(self.direction, self.BLOCK_SIZE)
        pygame.time.delay(self.UPDATE_SPEED)
            
        if (self.simulate):
            self.render()
            
        self.collision()