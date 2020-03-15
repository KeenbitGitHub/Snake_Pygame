import pygame
import snake
import food
import collision_detection
import numpy as np

class Game:
    def __init__(self, simulate):
        self.initialize(simulate)
        self.main()
    
    # Initializes variables
    def initialize(self, simulate):
        self.simulate = simulate
        self.BLOCK_WIDTH, self.BLOCK_HEIGHT = 50, 50 
        self.BLOCK_SIZE = (self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.WIN_WIDTH, self.WIN_HEIGHT = 800, 800
        self.WIN_SIZE = (self.WIN_WIDTH, self.WIN_HEIGHT)
        self.direction = (1, 0)
        self.snake_instance = snake.Snake((self.WIN_WIDTH/2, self.WIN_HEIGHT/2), 4, self.BLOCK_SIZE)
        self.food_instance = food.Food(self.snake_instance.body, self.WIN_SIZE, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
        self.collision_detection_instance = collision_detection.collision_detector()
        self.game_running = True
        
        pygame.init()
        
        if (self.simulate):
            self.win = pygame.display.set_mode(self.WIN_SIZE)
            self.CAPTION = "AI plays snake"
            pygame.display.set_caption(self.CAPTION)
        
        
    # Checks for player input
    def player_input(self):
        if (self.simulate):
            UPDATE_SPEED = 200
        else:
            UPDATE_SPEED = 2
        update_move = False
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.game_running = False
                UPDATE_SPEED = 0
                break
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT and self.direction != (1, 0) and not update_move):
                    self.direction = (-1, 0)
                    update_move = True
                elif (event.key == pygame.K_RIGHT and self.direction != (-1, 0) and not update_move):
                    self.direction = (1, 0)
                    update_move = True
                elif (event.key == pygame.K_DOWN and self.direction != (0, -1) and not update_move):
                    self.direction = (0, 1)
                    update_move = True
                elif (event.key == pygame.K_UP and self.direction != (0, 1) and not update_move):
                    self.direction = (0, -1)
                    update_move = True
        
        self.snake_instance.move(self.direction, self.BLOCK_SIZE)
        pygame.time.delay(UPDATE_SPEED)
        
        
    # Renders game
    def render(self):
        self.food_instance.render(self.BLOCK_WIDTH, self.BLOCK_HEIGHT, self.win)
        self.snake_instance.render(self.BLOCK_WIDTH, self.BLOCK_HEIGHT, self.win)
        pygame.display.update()
        
    # Checks for collision
    def collision(self):
        col_result = self.collision_detection_instance.check_collision(self.snake_instance.head, 
            self.snake_instance.body, self.WIN_SIZE, self.BLOCK_SIZE, self.food_instance)
        
        if (col_result == 1):
            self.snake_instance.alive = False
        elif (col_result == 2):
            self.food_instance.respawn(self.snake_instance.body, self.WIN_SIZE, self.BLOCK_SIZE[0], self.BLOCK_SIZE[1])
            self.snake_instance.body = np.append(self.snake_instance.body, self.snake_instance.moved_from).reshape((-1, 2))

    # Starts the game and the game-loop
    def main(self):
        while self.snake_instance.alive and self.game_running:
            self.player_input()
            if (self.simulate):
                self.render()
            self.collision()