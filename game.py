import pygame
import snake
import food
import collision_detection
import numpy as np

class Game:    
    # Initializes variables
    def __init__(self, human_playes = True):
        self.human_playes = human_playes
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
        self.update_move = False
        self.score = 0
        
        pygame.init()
        
        self.CAPTION = "Snake"
        pygame.display.set_caption(self.CAPTION)
        
        if (self.human_playes):    
            self.main()
        
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
        
    # Removes dead snakes and leftover food from the screen
    def clear_screen(self):
        if (not self.snake_instance.alive):
            pygame.draw.rect(self.win, (0, 0, 0), (self.food_instance.position[0], self.food_instance.position[1], self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
            
            pygame.draw.rect(self.win, (0, 0, 0), (self.snake_instance.head[0], self.snake_instance.head[1], self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
            
            for part in self.snake_instance.body[1:]:
                pygame.draw.rect(self.win, (0, 0, 0), (part[0], part[1], self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
            
            pygame.draw.rect(self.win, (0, 0, 0), (self.snake_instance.moved_from[0], self.snake_instance.moved_from[1], self.BLOCK_WIDTH, self.BLOCK_HEIGHT))
            
    # Checks for collisions
    def check_collisions(self):
        col_result = self.collision_detection_instance.check_collision(self.snake_instance.head, 
            self.snake_instance.body, self.WIN_SIZE, self.BLOCK_SIZE, self.food_instance)
        
        if (col_result == 1): # Wall is hit or snake bites itself
            self.snake_instance.alive = False
            self.clear_screen()
        elif (col_result == 2): # If snake eats food
            self.food_instance.respawn(self.snake_instance.body, self.WIN_SIZE, self.BLOCK_SIZE[0], self.BLOCK_SIZE[1])
            self.snake_instance.body = np.append(self.snake_instance.body, self.snake_instance.moved_from).reshape((-1, 2))
            self.score += 1

    # Starts the game and the game-loop
    def main(self):
        if (self.human_playes):
            while self.snake_instance.alive:
                self.player_input()
                self.update_move = False
                self.UPDATE_SPEED = 5

                self.snake_instance.move(self.direction, self.BLOCK_SIZE)
                pygame.time.delay(self.UPDATE_SPEED)
                    
                self.render()
                self.check_collisions()
                
        else:
            self.update_move = False
            self.UPDATE_SPEED = 5

            self.snake_instance.move(self.direction, self.BLOCK_SIZE)
            pygame.time.delay(self.UPDATE_SPEED)
                
            self.render()    
            self.check_collisions()