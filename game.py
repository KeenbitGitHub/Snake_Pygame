import pygame
import snake
import food
import collision_detection
import numpy as np

def initialize():
    global WIN_SIZE, WIN_WIDTH, WIN_HEIGHT, CAPTION, game_running, snake_instance, food_instance, collision_detection_instance, win
    global BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_SIZE, direction
    
    pygame.init()
    
    BLOCK_WIDTH, BLOCK_HEIGHT = 50, 50 
    BLOCK_SIZE = (BLOCK_WIDTH, BLOCK_HEIGHT)
    
    WIN_WIDTH, WIN_HEIGHT = 800, 800
    WIN_SIZE = (WIN_WIDTH, WIN_HEIGHT)
    win = pygame.display.set_mode(WIN_SIZE)
    
    snake_instance = None
    food_instance = None
    collision_detection_instance = None
    direction = (1, 0)
    
    snake_instance = snake.Snake((WIN_WIDTH/2, WIN_HEIGHT/2), 4, BLOCK_SIZE)
    food_instance = food.Food(snake_instance.body, WIN_SIZE, BLOCK_WIDTH, BLOCK_HEIGHT)
    collision_detection_instance = collision_detection.collision_detector()
    
    CAPTION = "AI plays snake"
    pygame.display.set_caption(CAPTION)
    
    game_running = True
    
    
def player_input():
    global game_running, direction, BLOCK_SIZE
    UPDATE_SPEED = 400
    UPDATE_MOVE = False
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            game_running = False
            UPDATE_SPEED = 0
            break
        elif (event.type == pygame.KEYDOWN):
            if (event.key == pygame.K_LEFT and direction != (1, 0) and not UPDATE_MOVE):
                direction = (-1, 0)
                UPDATE_MOVE = True
            elif (event.key == pygame.K_RIGHT and direction != (-1, 0) and not UPDATE_MOVE):
                direction = (1, 0)
                UPDATE_MOVE = True
            elif (event.key == pygame.K_DOWN and direction != (0, -1) and not UPDATE_MOVE):
                direction = (0, 1)
                UPDATE_MOVE = True
            elif (event.key == pygame.K_UP and direction != (0, 1) and not UPDATE_MOVE):
                direction = (0, -1)
                UPDATE_MOVE = True
    
    snake_instance.move(direction, BLOCK_SIZE)
    pygame.time.delay(UPDATE_SPEED)
    
    
def render():
    global BLOCK_WIDTH, BLOCK_HEIGHT, snake_instance, win
    food_instance.render(BLOCK_WIDTH, BLOCK_HEIGHT, win)
    snake_instance.render(BLOCK_WIDTH, BLOCK_HEIGHT, win)
    pygame.display.update()
    
def collision():
    global snake_instance, food_instance, WIN_SIZE, BLOCK_SIZE
    col_result = collision_detection_instance.check_collision(snake_instance.head, snake_instance.body, WIN_SIZE, BLOCK_SIZE, food_instance)
    
    if (col_result == 1):
        snake_instance.alive = False
    elif (col_result == 2):
        food_instance.respawn(snake_instance.body, WIN_SIZE, BLOCK_SIZE[0], BLOCK_SIZE[1])
        snake_instance.body = np.append(snake_instance.body, snake_instance.moved_from).reshape((-1, 2))

def main():
    global game_running, snake_instance
    
    initialize()
    
    while snake_instance.alive and game_running:
        player_input()
        render()
        collision()
    
main()